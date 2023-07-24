from abc import ABC
from typing import List, Any

import numpy as np
import pandas as pd
from pandas import DataFrame
from uuid import uuid4

from src.file.converter.bicycle_simra.simra_bicycle_columns import SimraColumn
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AbstractColumnCalculator
from src.data_transfer.content import Column
from src.file.converter.util.data_util import repair_number_column, find_numeric_rows, DistanceCalculator


class IDCalculator(AbstractColumnCalculator):
    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def is_repairable(self, source_df: DataFrame) -> bool:
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        return True

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Generates a new datapoint id.
        :param source_df: the imported data frame
        :param result_df: the data frame to write into
        :returns true if successful
        """
        uuid_list = [uuid4() for _ in range(len(source_df))]
        result_df[Column.ID.value] = pd.DataFrame({"uuid": uuid_list})
        return True


class TrajectoryIDCalculator(AbstractColumnCalculator):
    """
    Since the data is made up of only one trajectory, the trajectory id is always the same.
    """

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def is_repairable(self, source_df: DataFrame) -> bool:
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        return True

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Generates a new trajectory id.
        :param source_df: the imported data frame
        :param result_df: the data frame to write into
        :returns true if successful
        """
        result_df[Column.TRAJECTORY_ID.value] = uuid4()
        return True


class GPSCalculator(AbstractColumnCalculator, ABC):
    def __init__(self, column: SimraColumn, result_column: Column, range: tuple = (-180, 180)):
        self.column = column
        self.result_column = result_column
        self.range = range

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        result_df[self.result_column.value] = source_df[self.column.value]
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        Repair the column by removing all rows with a faulty value. Faulty values are entries that
        are not of type float or double or are not in the range of the given range.
        """
        source_df.drop(source_df[~find_numeric_rows(source_df[self.column.value], self.range)].index, inplace=True)
        source_df.reset_index(drop=True, inplace=True)
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        Check if the column is repairable. The column is repairable if it contains at least one
        row that is of type float or double and is in the range of the given range.
        """
        return find_numeric_rows(source_df[self.column.value], self.range).any()

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        Find all fatal corruptions in the column. Fatal corruptions are entries that are not of type float
        or double or are not in the range of the given range.
        """
        return source_df[~find_numeric_rows(source_df[self.column.value], self.range)].index.tolist()

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return []


class LatitudeCalculator(GPSCalculator):
    def __init__(self, column: SimraColumn = SimraColumn.LATITUDE,
                 result_column: Column = Column.LATITUDE,
                 range: tuple = (-90, 90)):
        super().__init__(column, result_column, range)


class LongitudeCalculator(GPSCalculator):
    def __init__(self, column: SimraColumn = SimraColumn.LONGITUDE,
                 result_column: Column = Column.LONGITUDE,
                 range: tuple = (-180, 180)):
        super().__init__(column, result_column, range)


class DateTimeCalculator(AbstractColumnCalculator, ABC):

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        Repair the TimeStamp column by removing all rows with a faulty TimeStamp. Faulty TimeStamps are negative
        TimeStamps or entries that are not of type int.
        """
        source_df.drop(source_df[~source_df[SimraColumn.TIME_STAMP.value].astype(str).str.isdigit()].index,
                       inplace=True)
        source_df.drop(source_df[source_df[SimraColumn.TIME_STAMP.value] < 0].index, inplace=True)
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """The TimeStamp column is repairable if it contains at least one correct entry."""
        return source_df[SimraColumn.TIME_STAMP.value].astype(str).str.isdigit().any()

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        Any row with a faulty TimeStamp is a fatal corruption. Faulty TimeStamps are negative TimeStamps or entries
        that are not of type int.
        """
        not_int = source_df[~source_df[SimraColumn.TIME_STAMP.value].astype(str).str.isdigit()].index.tolist()
        invalid_int = source_df[source_df[SimraColumn.TIME_STAMP.value] < 0].index.tolist()
        # merge the two lists without duplicates
        return list(set(not_int + invalid_int))

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        If the TimeStamp column is not repairable, there are no repairable corruptions.
        """
        return []


class TimeCalculator(DateTimeCalculator):
    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Calculate the time of the day from the time stamp.
        """
        result_df[Column.TIME.value] = pd.to_datetime(source_df[SimraColumn.TIME_STAMP.value], unit='ms') \
            .dt.strftime('%H:%M:%S')
        return True


class DateCalculator(DateTimeCalculator):
    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Calculate the date from the time stamp.
        """
        result_df[Column.DATE.value] = pd.to_datetime(source_df[SimraColumn.TIME_STAMP.value], unit='ms') \
            .dt.strftime('%d.%m.%Y')
        return True


class SpeedCalculator(AbstractColumnCalculator):
    """
    Calculates the speed from the differences in the latitude and longitude columns and the time stamp.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        # calculate the speed from the differences in the latitude and longitude columns and the time stamp
        temp_df: pd.DataFrame = source_df[[SimraColumn.LATITUDE.value, SimraColumn.LONGITUDE.value,
                                           SimraColumn.TIME_STAMP.value]]
        distance_calculator = DistanceCalculator(lat_col=SimraColumn.LATITUDE.value, long_col=SimraColumn.LONGITUDE.value)
        temp_df["distance"] = distance_calculator.get_distance(temp_df)
        temp_df[SimraColumn.TIME_STAMP.value] = temp_df[SimraColumn.TIME_STAMP.value].diff()
        temp_df[SimraColumn.TIME_STAMP.value] = temp_df[SimraColumn.TIME_STAMP.value] / 1000
        temp_df["distance"] = temp_df["distance"] / temp_df[SimraColumn.TIME_STAMP.value]
        temp_df["distance"] = temp_df["distance"] * 3.6
        result_df[Column.SPEED.value] = temp_df["distance"]
        # add value for first row
        result_df[Column.SPEED.value].iloc[0] = 0
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        return True

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return []


class ConstantConverter(AbstractColumnCalculator):
    """
    Fills values in the given column with the given value.
    """

    def __init__(self, column: Column, value: Any):
        self.column = column
        self.value = value

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Fill the given column with the given value.
        """
        result_df[self.column.value] = self.value
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        The column is always repairable.
        """
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        The column is always repairable.
        """
        return True

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The column has no fatal corruptions.
        """
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The column has no repairable corruptions.
        """
        return []


class AccelerationCalculator(AbstractColumnCalculator, ABC):
    def repair_column(self, source_df: DataFrame) -> bool:
        """
        All values in the acceleration column are repairable. If the acceleration column is empty, it is repaired by
        filling it with zeros. Invalid values are replaced with zeros.
        """
        # replace all non numeric values with None
        source_df[SimraColumn.X.value] = repair_number_column(column_frame=source_df[SimraColumn.X.value],
                                                              def_value=0)
        source_df[SimraColumn.Y.value] = repair_number_column(column_frame=source_df[SimraColumn.Y.value],
                                                              def_value=0)
        source_df[SimraColumn.Z.value] = repair_number_column(column_frame=source_df[SimraColumn.Z.value],
                                                              def_value=0)
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        The acceleration column is always repairable.
        """
        return True

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The acceleration column has no fatal corruptions.
        """
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The acceleration column has no repairable corruptions.
        """
        return []


class AccelerationMagnitudeCalculator(AccelerationCalculator):
    """
    Calculates the acceleration from the acceleration_x, acceleration_y and acceleration_z columns.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Calculate the acceleration from the acceleration_x, acceleration_y and acceleration_z columns.
        """
        result_df[Column.ACCELERATION.value] = np.sqrt(np.square(source_df[SimraColumn.X.value]) +
                                                       np.square(source_df[SimraColumn.Y.value]) +
                                                       np.square(source_df[SimraColumn.Z.value]))
        return True


class AccelerationDirectionCalculator(AccelerationCalculator):
    """
    Calculates the acceleration direction from the acceleration_x, acceleration_y and acceleration_z columns.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Calculate the acceleration direction from the acceleration_x, acceleration_y and acceleration_z columns.
        """
        result_df[Column.ACCELERATION_DIRECTION.value] = np.arctan2(source_df[SimraColumn.Y.value],
                                                                    source_df[SimraColumn.X.value])
        return True


class SpeedDirectionCalculator(AbstractColumnCalculator):
    """
    Calculates the speed direction by using an approximation of the direction of the movement.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Calculate the speed direction by using an approximation of the direction of the movement.
        """
        result_df[Column.SPEED_DIRECTION.value] = np.arctan2(source_df[SimraColumn.LATITUDE.value].diff(),
                                                             source_df[SimraColumn.LONGITUDE.value].diff())
        # also calculate the speed direction for the first row
        result_df[Column.SPEED_DIRECTION.value].iloc[0] = np.arctan2(source_df[SimraColumn.LATITUDE.value].iloc[0],
                                                                     source_df[SimraColumn.LONGITUDE.value].iloc[0])

        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        The speed direction column is not present in the source data frame, so there is nothing to repair.
        """
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        The speed direction column is not present in the source data frame, so it is always repairable.
        """
        return True

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The speed direction column is not present in the source data frame, so there are no fatal corruptions.
        Or more precisely: If there are fatal corruptions, they are in the latitude or longitude column.
        So the fatal corruptions are found in the latitude or longitude column.
        """
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The speed direction column is not present in the source data frame, so there are no repairable corruptions.
        """
        return []
