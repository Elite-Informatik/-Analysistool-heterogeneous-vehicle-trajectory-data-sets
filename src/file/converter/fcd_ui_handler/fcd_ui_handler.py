import re
from abc import ABC
from abc import abstractmethod
from typing import List
from uuid import uuid4

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series

from src.data_transfer.content import Column
from src.data_transfer.content.road_type import VehicleType
from src.file.converter.fcd_ui_handler.fcd_columns import FcdColumn
from src.file.converter.util.data_util import DistanceCalculator
from src.file.converter.util.data_util import find_non_date_rows
from src.file.converter.util.data_util import find_non_numeric_rows
from src.file.converter.util.data_util import repair_number_column
from src.file.converter.util.data_util import repair_string_column

ms_to_kmh = 3.6


class AbstractFcdUiCalculator(ABC):
    """
    this abstract calculator represents a calculator responsible to calculate one column of our unified dataformat
    """

    @abstractmethod
    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        calculates and transfers the column from the source df into the result df
        :param source_df:   the source df
        :param result_df:   the result df
        :return:            whether the calculation was successful
        """
        pass

    @abstractmethod
    def repair_column(self, source_df: DataFrame) -> bool:
        """
        repairs the columns in the fcd ui dataset that are needed for calculation
        :param source_df:   the source df
        :return:            whether the repairing was successful
        """
        pass

    @abstractmethod
    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        checks whether the column can be repaired or has to be marked as invalid
        :param source_df:   the source df
        :return             whether the column can be repaired
        """
        raise NotImplementedError

    @abstractmethod
    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        searches for fatal corruptions that cant be repaired so that the row has to be deleted
        :param source_df:   the source df
        :return:            the list of row indices that have to be deleted
        """
        raise NotImplementedError

    @abstractmethod
    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        searches for repairable corruptions that can be repaired
        :param source_df:   the source df
        :return:            the list of row indices that have repairable corruptions
        """
        raise NotImplementedError


class IdCalculator(AbstractFcdUiCalculator):
    """
    This calculator calculates the datapoint ID
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
        Generates a new datapoint id.
        :param source_df: the imported data frame
        :param result_df: the data frame to write into
        :returns true if successful
        """
        uuid_list = [uuid4() for _ in range(len(source_df))]
        result_df[Column.ID.value] = pd.DataFrame({"uuid": uuid_list})
        return True


class TrajectoryIDCalculator(AbstractFcdUiCalculator):
    """
    This calculator calculates the trajectory ID
    """

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        repairable_corruptions: List[int] = []
        length_column = source_df[FcdColumn.TRIP.value].shape[0]
        # corrupt_indices = source_df[~source_df[FcdColumn.TRIP.value].str.match("-?\d+")].index
        corrupt_indices = find_non_numeric_rows(source_df[FcdColumn.TRIP.value])
        for index in corrupt_indices:
            if index != 0 and index != (length_column - 1) and (
                    source_df.at[index - 1, FcdColumn.TRIP.value] ==
                    source_df.at[index + 1, FcdColumn.TRIP.value] and not (index + 1) in corrupt_indices):
                repairable_corruptions.append(index)
        return repairable_corruptions

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        fatal_corruptions: List[int] = []
        length_column = source_df[FcdColumn.TRIP.value].shape[0]
        # corrupt_indices = source_df[~source_df[FcdColumn.TRIP.value].str.match("-?\d+")].index
        corrupt_indices = find_non_numeric_rows(source_df[FcdColumn.TRIP.value])
        for index in corrupt_indices:
            if index == 0 or index == (length_column - 1):
                fatal_corruptions.append(index)
            elif not (source_df.at[index - 1, FcdColumn.TRIP.value] ==
                      source_df.at[index + 1, FcdColumn.TRIP.value] and not (index + 1) in corrupt_indices):
                fatal_corruptions.append(index)
        return fatal_corruptions

    def repair_column(self, source_df: DataFrame) -> bool:
        indices_to_repair = source_df[~source_df[FcdColumn.TRIP.value].str.match("-?\d+")].index
        for index in indices_to_repair:
            source_df.at[index, FcdColumn.TRIP.value] = source_df.at[
                index + 1, FcdColumn.TRIP.value]
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        # string_df = source_df[FcdColumn.TRIP.value].str
        # return source_df[FcdColumn.TRIP.value].str.match(r"-?\d+").any()
        return source_df[FcdColumn.TRIP.value].apply(pd.to_numeric, errors="coerce").notna().any()

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        calculates the trajectory ID column and inserts it in the result_df. It maps the trip id to a new uuid
        """
        unique_trajectories = source_df[FcdColumn.TRIP.value].unique()
        trajectory_id_dict = {}
        for i in range(len(unique_trajectories)):
            trajectory_id_dict[unique_trajectories[i]] = uuid4()
        result_df[Column.TRAJECTORY_ID.value] = source_df[FcdColumn.TRIP.value].map(trajectory_id_dict)
        return True


class DateTimeCalculator(AbstractFcdUiCalculator, ABC):
    """
    this calculator calculates the data and the time
    """

    column = FcdColumn.DATE_TIME.value
    ns_to_seconds = 1000000000

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return find_non_date_rows(source_df[self.column])

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        Finds the rows that cannot easily be repaired in the column.
        :param source_df: The FCD UI data that is checked for inconsistency.
        :return: A list of the row numbers, that need to be deleted.
        """
        fatal_lines: List[int] = []
        # inspect each trajectory individually.
        for (_, trajectory_df) in source_df.groupby(FcdColumn.TRIP.value):

            trajectory_df_start: int = trajectory_df.index[0]
            start_value_index = 0
            end_value_index = trajectory_df.shape[0] - 1
            # add the start/end index to the fatal_lines while they are invalid
            while True:
                first_invalid = pd.isna(
                    pd.to_datetime(trajectory_df[self.column].iloc[start_value_index], errors='coerce'))
                last_invalid = pd.isna(
                    pd.to_datetime(trajectory_df[self.column].iloc[end_value_index], errors='coerce'))
                if end_value_index - start_value_index == 0:
                    if first_invalid:
                        fatal_lines.append(start_value_index + trajectory_df_start)
                    break
                if end_value_index - start_value_index < 0:
                    break
                if first_invalid:
                    fatal_lines.append(start_value_index + trajectory_df_start)
                    start_value_index += 1
                if last_invalid:
                    fatal_lines.append(end_value_index + trajectory_df_start)
                    end_value_index -= 1
                if not first_invalid and not last_invalid:
                    break

            # find all other corrupted indexes.
            invalid_indices = \
                trajectory_df[self.column][pd.to_datetime(trajectory_df[self.column], errors='coerce').isna()].index
            if len(invalid_indices) == 0:
                continue

            # discard an invalid line if the next line is also invalid, as the average cannot be calculated if a row
            # above or below is invalid.
            prev_idx = invalid_indices[0]
            for idx in invalid_indices:
                if idx - prev_idx == 1:
                    fatal_lines.append(prev_idx)
                prev_idx = idx
        # return the fatal_lines as set, as a line can qualify for multiple corruptions.
        return list(set(fatal_lines))

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        The method checks if there is at least one valid entry in the column.
        :param source_df: The FCD UI data to be checked.
        :return: True if the Dataframe is repairable, False if not.
        """
        if FcdColumn.TRIP.value not in source_df.columns or FcdColumn.DATE_TIME.value not in source_df.columns:
            return False

        valid_indices = \
            source_df[self.column][pd.to_datetime(source_df[self.column], errors='coerce').notna()].index
        return len(valid_indices) > 0

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        Repairs the time column by taking the average of the date_time above and below for each trajectory.
        :param source_df:   the source df
        :return:            whether the repairing was successful
        """
        invalid_indices = \
            source_df[self.column][pd.to_datetime(source_df[self.column], errors='coerce').isna()].index

        for idx in invalid_indices.to_list():
            prev_value = pd.to_datetime(source_df.at[idx - 1, self.column])  # .value / self.ns_to_seconds
            next_value = pd.to_datetime(source_df.at[idx + 1, self.column])  # .value / self.ns_to_seconds
            avg = prev_value + (next_value - prev_value) / 2
            avg = pd.to_datetime(avg).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            source_df.at[idx, self.column] = avg

        return True


class DateCalculator(DateTimeCalculator):
    """
    This calculator calculates the Date.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        # convert the datetime to date
        result_df[Column.DATE.value] = pd.to_datetime(source_df[self.column]).dt.strftime('%d.%m.%Y')
        return True


class TimeCalculator(DateTimeCalculator):
    """
    This calculator calculates the Time.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        # convert the datetime to date
        result_df[Column.TIME.value] = pd.to_datetime(source_df[self.column]).dt.strftime('%H:%M:%S')
        return True


class SpeedCalculator(AbstractFcdUiCalculator):
    """
    this calculator calculates the speed
    """

    column = FcdColumn.SPEED.value

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        result_df[Column.SPEED.value] = source_df[self.column]
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        if self.column in source_df.columns and len(source_df[self.column]
                                                    [pd.to_numeric(source_df[self.column],
                                                                   errors='coerce').notna()].index) > 0:
            source_df[self.column] = repair_number_column(source_df[self.column], def_value=0, linear_transition=True)
            return True
        temp_df = DataFrame()
        GpsCoordinateCalculator().calculate_column(source_df, temp_df)
        temp_df['id'] = source_df[FcdColumn.TRIP.value]
        distance_calculator = DistanceCalculator(lat_col=Column.LATITUDE.value, long_col=Column.LONGITUDE.value)
        temp_df['distance'] = temp_df.groupby('id').apply(distance_calculator.get_distance).transpose()

        temp_df['time_diff'] = pd.to_datetime(source_df[FcdColumn.DATE_TIME.value]).diff()
        if FcdColumn.SPEED.value not in source_df.columns:
            source_df[FcdColumn.SPEED.value] = [None] * source_df.shape[0]
        # calculate the speed via distance / delta_time
        source_df[FcdColumn.SPEED.value] = np.where(source_df[FcdColumn.SPEED.value].isna(),
                                                    1 / ((temp_df['time_diff']) / temp_df['distance']
                                                         / pd.Timedelta(seconds=1)),
                                                    source_df[FcdColumn.SPEED.value])
        # convert the speed to km/h
        source_df[FcdColumn.SPEED.value] = source_df[FcdColumn.SPEED.value] * ms_to_kmh
        source_df[self.column] = repair_number_column(source_df[self.column], def_value=0, linear_transition=True)
        source_df[self.column] = source_df[self.column].round(1)
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        if self.column in source_df.columns and len(source_df[self.column]
                                                    [pd.to_numeric(source_df[self.column],
                                                                   errors='coerce').notna()].index) > 0:
            return True
        if TimeCalculator().is_repairable(source_df) and GpsCoordinateCalculator().is_repairable(source_df) \
                and TrajectoryIDCalculator().is_repairable(source_df):
            return True
        return False

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        if self.column not in source_df.columns:
            source_df[self.column] = pd.Series(dtype=float)
        return find_non_numeric_rows(source_df[self.column])


class SpeedLimitCalculator(AbstractFcdUiCalculator):
    """
    this calculator calculates the speed limit
    """

    column = FcdColumn.MAX_SPEED.value

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return find_non_numeric_rows(source_df[self.column])

    def contains_number(self, group: Series):
        """
        function to check whether a group contains a number
        """
        group = pd.to_numeric(group, errors='coerce')
        return group.notna()

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        Finds all the fatal corruptions. Fatal corruptions are those where for the given segement of road_type not a
        single max speed is given.
        :param source_df: The FCD UI Dataframe to check.
        :return: List[int] of the rows that need to be deleted.
        """
        source_df['valid_group'] = source_df.groupby(FcdColumn.ROAD_TYPE.value)[self.column].apply(
            self.contains_number)
        source_df.replace(to_replace=False, value=None, inplace=True)
        source_df['valid_group'] = source_df.groupby(FcdColumn.ROAD_TYPE.value)['valid_group'] \
            .transform(lambda x: x.fillna(x.mean())) \
            .replace(to_replace=1.0, value=True) \
            .fillna(False)

        # get all the lines that contain False
        invalid_lines: List[int] = source_df[~source_df.valid_group].index.to_list()
        return invalid_lines

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        result_df[Column.SPEED_LIMIT.value] = source_df[self.column]
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        # Delete all entries that are not a number
        source_df[self.column] = pd.to_numeric(source_df[self.column], errors='coerce')

        # Fill missing values forward and backward to propagate the last valid value
        source_df[self.column] = source_df[self.column].ffill().bfill()

        # Check if the last and next valid value are the same
        source_df['check'] = (source_df[self.column].shift(1) == source_df[self.column].shift(-1))

        # Fill missing values with the same value if the last and next valid value are the same
        source_df[self.column] = np.where(source_df['check'], source_df[self.column].bfill(), source_df[self.column])
        source_df.drop(columns=['check'], inplace=True)
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        Checks if the column is repairable.
        It is not repairable if the column is not in the source_df or if the road_type column is not in the source_df.
        It is also not repairable if there are not a single valid values in the column.
        :param source_df:
        :return:
        """
        if self.column not in source_df.columns or FcdColumn.ROAD_TYPE.value not in source_df.columns:
            return False
        valid_limits = source_df[self.column][pd.to_numeric(source_df[self.column], errors='coerce').notna()].index
        return len(valid_limits) > 0


class AccelerationCalculator(AbstractFcdUiCalculator):
    """
    Calculates the Acceleration from the time and the speed column.
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Performs the calculation of the acceleration column.
        :param source_df: The FCD UI data frame
        :param result_df: The data frame in which our data is written.
        :returns True if successful.
        """
        temp_df = DataFrame()
        temp_df['id'] = source_df[FcdColumn.TRIP.value]
        temp_df['speed'] = source_df[FcdColumn.SPEED.value] / ms_to_kmh
        temp_df['time_diff'] = pd.to_datetime(source_df[FcdColumn.DATE_TIME.value])
        temp_df['speed_diff'] = pd.to_numeric(temp_df['speed']).diff()
        temp_df['time_diff'] = temp_df.groupby('id')['time_diff'].diff()
        temp_df['time_diff'] = (1 /
                                (temp_df['time_diff']
                                 / temp_df['speed_diff']
                                 / pd.Timedelta(seconds=1)))
        result_df[Column.ACCELERATION.value] = temp_df['time_diff'].replace({np.inf: 0})
        result_df[Column.ACCELERATION.value] = result_df[Column.ACCELERATION.value].bfill()
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        The column cannot be repaired as it does not exist.
        :param source_df: The fcd data.
        :returns True
        """
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        The column is always repairable, as it is always calculated.
        :param source_df: The FCD UI data
        :returns True
        """
        return True  # Speed as well as time are checked beforehand.
        # If they are not valid the data cannot be read anyway.

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The column has no fatal corruptions as it does not exist in the source FCD UI data.
        :param source_df: FCD UI data in a pandas Dataframe.
        :return: empty list
        """
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The column has no repairable corruptions as it does not exist in the source FCD UI data.
        :param source_df: FCD UI data in a pandas Dataframe.
        :return: empty list
        """
        return []


class GpsCoordinateCalculator(AbstractFcdUiCalculator):
    """
    This calculator calculates the GPS coordinates (latitude and longitude)
    """

    COORDINATE_REGEX = r"POINT\s\((\d+(?:\.\d+)?)\s(\d+(?:\.\d+)?)\)"

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        # cant be repaired
        return []

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return source_df[~source_df[FcdColumn.POINT.value].str.match(self.COORDINATE_REGEX)].index

    def is_repairable(self, source_df: DataFrame) -> bool:
        if FcdColumn.POINT.value not in source_df.columns:
            return False
        return source_df[FcdColumn.POINT.value].str.match(self.COORDINATE_REGEX).any()

    def repair_column(self, source_df: DataFrame) -> bool:
        # cant be repaired
        return True

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        calculates the longitude and latitude column and inserts it in the result_df
        """
        result_df[[Column.LONGITUDE.value, Column.LATITUDE.value]] = source_df[FcdColumn.POINT.value] \
            .str.extract(pat=self.COORDINATE_REGEX, expand=True).astype(float)
        return True


class SpeedDirectionCalculator(AbstractFcdUiCalculator):
    """
    This calculator calculates the speed direction
    """

    def repair_column(self, source_df: DataFrame) -> bool:
        azimuth_colum = FcdColumn.AZIMUTH.value
        temp_df = DataFrame()

        source_df[azimuth_colum] = source_df[azimuth_colum].apply(pd.to_numeric, errors='coerce')
        source_df[azimuth_colum] = np.where(((source_df[azimuth_colum] >= 0) & (source_df[azimuth_colum] <= 360)),
                                            source_df[azimuth_colum],
                                            np.nan)
        GpsCoordinateCalculator().calculate_column(source_df=source_df, result_df=temp_df)
        temp_df['azimuth'] = DataFrame(
            np.degrees(np.arctan2(0 - temp_df[Column.LONGITUDE.value].diff(),
                                  0 - temp_df[Column.LATITUDE.value].diff()))
        ) % 360
        source_df[FcdColumn.AZIMUTH.value] = np.where(source_df[azimuth_colum].isna(),
                                                      temp_df['azimuth'],
                                                      source_df[FcdColumn.AZIMUTH.value])
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        Checks if the column is repairable.
        The column is always repairable, as it can be calculated from the gps coordinates. These are checked beforehand.
        :param source_df: The FCD UI data in a pandas Dataframe.
        :return: True
        """
        return True

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        # you can calculate every entry out of the gps coordinates
        return []

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        calculates the speed direction column and inserts it in the result_df
        """
        result_df[Column.SPEED_DIRECTION.value] = source_df[FcdColumn.AZIMUTH.value].astype(float)
        return True


class AccelerationDirectionCalculator(AbstractFcdUiCalculator):
    """
    calculates the acceleration direction column
    """

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        # calculate speed vector 1
        temp_df = DataFrame()
        temp_df['x1'] = source_df[FcdColumn.SPEED.value] * np.cos(np.radians(source_df[FcdColumn.AZIMUTH.value]))
        temp_df['y1'] = source_df[FcdColumn.SPEED.value] * np.sin(np.radians(source_df[FcdColumn.AZIMUTH.value]))
        # calculate speed vector 2
        temp_df['x2'] = source_df[FcdColumn.SPEED.value].shift(-1) * np.cos(
            np.radians(source_df[FcdColumn.AZIMUTH.value].shift(-1)))
        temp_df['y2'] = source_df[FcdColumn.SPEED.value].shift(-1) * np.sin(
            np.radians(source_df[FcdColumn.AZIMUTH.value].shift(-1)))
        # calculate acceleration vector
        temp_df['x3'] = temp_df['x2'] - temp_df['x1']
        temp_df['y3'] = temp_df['y2'] - temp_df['y1']
        # calculate acceleration direction
        result_df[Column.ACCELERATION_DIRECTION.value] = np.degrees(np.arctan2(temp_df['y3'], temp_df['x3'])) % 360
        result_df[Column.ACCELERATION_DIRECTION.value].fillna(0, inplace=True)
        return False

    def repair_column(self, source_df: DataFrame) -> bool:
        # nothing to repair since this column completely depends on speed and the speed direction
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        # if repairable completely depends on speed and speed direction
        return True

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return []


class RoadTypeCalculator(AbstractFcdUiCalculator):
    """
    This calculator calculates the road type
    """

    def is_repairable(self, source_df: DataFrame) -> bool:
        return ((source_df[FcdColumn.ROAD_TYPE.value] != '') & (source_df[FcdColumn.ROAD_TYPE.value].notnull())).any()

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return source_df[
            source_df[FcdColumn.ROAD_TYPE.value].isna() | source_df[FcdColumn.ROAD_TYPE.value].str.match("^$")].index

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def repair_column(self, source_df: DataFrame) -> bool:
        source_df[FcdColumn.ROAD_TYPE.value] = repair_string_column(
            DataFrame(source_df[FcdColumn.ROAD_TYPE.value]), re.compile(r'(.*?)'))
        return True

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        calculates the road type column and inserts it in the result_df
        """
        result_df[Column.ROAD_TYPE.value] = source_df[FcdColumn.ROAD_TYPE.value]
        return True


class OSMRoadIDCalculator(AbstractFcdUiCalculator):
    """
    This calculator calculates the OSM road ID
    """

    def repair_column(self, source_df: DataFrame) -> bool:
        source_df[FcdColumn.ROAD_OSM_TYPE.value] = repair_string_column(
            DataFrame(source_df[FcdColumn.ROAD_OSM_TYPE.value]), re.compile(r"-?\d+"))
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        return source_df[FcdColumn.ROAD_OSM_TYPE.value].apply(pd.to_numeric, errors="coerce").notna().any()

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        return find_non_numeric_rows(source_df[FcdColumn.ROAD_OSM_TYPE.value])

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        return []

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        calculates the OSM road ID column and inserts it in the result_df
        """
        result_df[Column.OSM_ROAD_ID.value] = source_df[FcdColumn.ROAD_OSM_TYPE.value].astype(int)
        return True


class VehicleTypeCalculator(AbstractFcdUiCalculator):
    """
    this calculator calculates the vehicle type
    """

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        The vehicle type is always repairable as the vehicle type is always unknown.
        :param source_df: the source FCD UI dataframe
        :return: True
        """
        return True

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The vehicle type is always repairable as the vehicle type is always unknown. Therefore, there are no repairable
        corruptions.
        :param source_df:
        :return: empty list
        """
        return []

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        The vehicle type is column has no corruptions vehicle type is always unknown. Therefore, there are no fatal
        corruptions.
        :param source_df: the source FCD UI dataframe
        :return: empty list
        """
        return []

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        The vehicle type is always repairable as the vehicle type is always unknown.
        Therefore, there is nothing to repair.
        :param source_df: the source FCD UI dataframe
        :return: True
        """
        return True

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        The vehicle type is always unknown. Therefore, the vehicle type is set to unknown.
        :param source_df: the source FCD UI dataframe
        :param result_df: the destination dataframe of the unified data format
        :return: True if successful
        """
        result_df[Column.VEHICLE_TYPE.value] = VehicleType.UNKNOWN.value
        return True


class OneWayStreetCalculator(AbstractFcdUiCalculator):
    """
    Transfers the one way column from the FCD UI data to the unified data format.
    """
    column = FcdColumn.ONE_WAY_STREET.ONE_WAY_STREET.value

    def calculate_column(self, source_df: DataFrame, result_df: DataFrame) -> bool:
        """
        Transfers the column over.
        :param source_df: The FCD UI data as a pandas dataframe.
        :param result_df: The resulting data as a pandas dataframe in which the data is written into.
        :returns True if successful
        """
        result_df[Column.ONE_WAY_STREET.value] = source_df[self.column]
        return True

    def repair_column(self, source_df: DataFrame) -> bool:
        """
        Repairs the column by first forward propagating and then backward propagating the missing values.
        :param source_df: The FCD UI data as a pandas DataFrame that is supposed to be repaired.
        :returns True if successful
        """
        source_df[self.column] = source_df[self.column].replace({"TRUE": True, "None": False, "FALSE": False,
                                                                 "True": True, "False": False})
        source_df[self.column] = source_df[self.column].apply(pd.to_numeric, errors='coerce')

        source_df[self.column] = source_df[self.column].ffill().bfill()
        return True

    def is_repairable(self, source_df: DataFrame) -> bool:
        """
        Checks if the column is repairable. The column is repairable if it contains only boolean values.
        None is interpreted as False.
        :param source_df: the FCD UI data as a pandas DataFrame
        :return: True if the column is repairable
        """
        return source_df[self.column].isin([True, False, "NONE"]).any()

    def find_fatal_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        Finds the fatal corruptions in the column. As the column is not too important, no fatal corruptions are found.
        :param source_df: the FCD UI data as a pandas DataFrame
        :return: an empty list
        """
        return []

    def find_repairable_corruptions(self, source_df: DataFrame) -> List[int]:
        """
        Finds the repairable corruptions in the column. A repairable corruption is a value that is not a boolean value.
        :param source_df: The FCD UI data as a pandas DataFrame
        :return: a list of indices of the rows that contain a repairable corruption
        """
        return source_df[~source_df[self.column].isin([True, False])].index.to_list()
    # todo: fixed all lines as corrupt -> why not visible when reading data set?
