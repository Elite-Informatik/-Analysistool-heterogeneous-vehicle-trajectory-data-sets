from typing import Dict
from typing import List
from typing import Tuple

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.content.data_types import DataTypes
from src.data_transfer.exception import ExecutionFlowError
from src.data_transfer.record import DataRecord
from src.file.converter.data_converter import DataConverter
from src.file.converter.fcd_ui_handler.fcd_columns import FcdColumn
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AbstractColumnCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AccelerationCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AccelerationDirectionCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import DateCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import GpsCoordinateCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import IdCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import OSMRoadIDCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import OneWayStreetCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import RoadTypeCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import SpeedCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import SpeedDirectionCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import SpeedLimitCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import TimeCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import TrajectoryIDCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import VehicleTypeCalculator


class FCDUIConverter(DataConverter):
    """
    this converter converts datasets in the fcd ui format into the unified data format
    """

    REQ_COLUMNS: List[str] = [FcdColumn.TRIP.value, FcdColumn.DATE_TIME.value, FcdColumn.POINT.value]
    OPT_COLUMNS: List[str] = [FcdColumn.SPEED.value, FcdColumn.MAX_SPEED.value, FcdColumn.AZIMUTH.value,
                              FcdColumn.ROAD_TYPE.value, FcdColumn.ROAD_OSM_TYPE.value, FcdColumn.ONE_WAY_STREET.value]

    NAME: str = DataTypes.FCD_UI.value
    SEPARATOR: str = ", "
    INVALID_COLUMN_STR: str = "The following Columns are invalid: "
    REPAIRABLE_CORRUPTIONS_STR: str = "The following rows are corrupted but repairable: "
    FATAL_CORRUPTIONS_STR: str = "The following rows are corrupted but not repairable and will be deleted: "

    def __init__(self):
        """
        Constructor for a new FCD UI Converter
        """
        self.is_valid = False
        self.handler_map: Dict[Column, AbstractColumnCalculator] = {
            Column.ID: IdCalculator(),
            Column.TRAJECTORY_ID: TrajectoryIDCalculator(),
            Column.DATE: DateCalculator(),
            Column.TIME: TimeCalculator(),
            Column.LATITUDE: GpsCoordinateCalculator(),
            Column.SPEED: SpeedCalculator(),
            Column.SPEED_LIMIT: SpeedLimitCalculator(),
            Column.ACCELERATION: AccelerationCalculator(),
            Column.SPEED_DIRECTION: SpeedDirectionCalculator(),
            Column.ACCELERATION_DIRECTION: AccelerationDirectionCalculator(),
            Column.ROAD_TYPE: RoadTypeCalculator(),
            Column.OSM_ROAD_ID: OSMRoadIDCalculator(),
            Column.ONE_WAY_STREET: OneWayStreetCalculator(),
            Column.VEHICLE_TYPE: VehicleTypeCalculator()
        }
        self.invalid_columns: List[Column] = []
        # self.repairable_corruptions: List[int] = []
        self.repairable_corruptions: List[Tuple[Column, List[int]]] = []
        self.fatal_corruptions: List[int] = []

    def convert_to_data(self, data: List[DataRecord]) -> DataRecord:
        """
        converts the given fcd ui dataset into the unified dataformat
        :param data:    the fcd ui dataframe
        :return:        the unified dataset
        """
        if not self.is_valid:
            raise \
                ExecutionFlowError(f"The Dataset has not been validated by the {self.is_convertable.__name__} method.")
        source_df: pd.DataFrame = data[0].data  # fcd ui dataframe consists of only one dataframe
        source_df = self.trim_data_set(source_df)
        destination_df: pd.DataFrame = pd.DataFrame()

        # delete all rows with fatal corruptions
        source_df = source_df.drop(index=self.fatal_corruptions)
        self.fatal_corruptions = []
        source_df.reset_index(drop=True, inplace=True)
        source_df = source_df.astype(str)
        # repair all columns following the dependencies between them
        for column in [column for column in
                       [Column.ID, Column.TRAJECTORY_ID, Column.DATE, Column.TIME, Column.LATITUDE, Column.SPEED_LIMIT,
                        Column.ROAD_TYPE, Column.OSM_ROAD_ID, Column.ONE_WAY_STREET, Column.VEHICLE_TYPE]
                       if column not in self.invalid_columns]:
            self.handler_map[column].repair_column(source_df)
        for column in [column for column in [Column.SPEED_DIRECTION, Column.SPEED]
                       if column not in self.invalid_columns]:
            self.handler_map[column].repair_column(source_df)
        for column in [column for column in [Column.ACCELERATION, Column.ACCELERATION_DIRECTION]
                       if column not in self.invalid_columns]:
            self.handler_map[column].repair_column(source_df)

        # transfer each column into the destination_df
        for column, calculator in self.handler_map.items():
            calculator.calculate_column(source_df=source_df, result_df=destination_df)
        destination_df[Column.FILTERED.value] = False

        # create a order column
        destination_df[Column.ORDER.value] = destination_df.reset_index()['index']

        # fill all remaining columns with default values
        for column in [column.value for column in Column if column.value not in destination_df.columns]:
            destination_df[column] = None

        return DataRecord("new fcd ui dataset", (), destination_df)

    def get_data_format(self) -> str:
        return self.NAME

    def is_convertable(self, data: List[DataRecord]) -> bool:
        if len(data) != 1:
            return False
        data_df = data[0].data
        if not all((column in data_df.columns) for column in self.REQ_COLUMNS):
            # df contains all required columns?
            return False
        if not all((self.handler_map[column].is_repairable(data_df)) for column in
                   [Column.TIME, Column.DATE, Column.TRAJECTORY_ID, Column.LATITUDE]):
            # all required columns repairable?
            return False
        self.is_valid = True
        return True

    def search_inaccuracies(self, data: List[DataRecord]) -> List[str]:
        returned_inaccuracies: List[str] = []
        data_df = self.trim_data_set(data[0].data)
        for column, calculator in self.handler_map.items():
            if not calculator.is_repairable(data_df):
                self.invalid_columns.append(column)

        for column, calculator in self.handler_map.items():
            repairable_corruptions = calculator.find_repairable_corruptions(data_df)
            if len(repairable_corruptions) > 0:
                self.repairable_corruptions.extend([(column, calculator.find_repairable_corruptions(data_df))])
            # self.repairable_corruptions.extend(calculator.find_repairable_corruptions(data_df))
        # self.repairable_corruptions = list(set(self.repairable_corruptions))

        for column, calculator in self.handler_map.items():
            self.fatal_corruptions.extend(calculator.find_fatal_corruptions(data_df))
        self.fatal_corruptions = list(set(self.fatal_corruptions))

        if len(self.invalid_columns) > 0:
            invalid_columns_string: str = self.SEPARATOR.join([column.value for column in self.invalid_columns])
            returned_inaccuracies.append(self.INVALID_COLUMN_STR + invalid_columns_string)

        if len(self.repairable_corruptions) > 0:
            repairable_corruptions_string: str = self.SEPARATOR.join([str(row) for row in self.repairable_corruptions])
            returned_inaccuracies.append(self.REPAIRABLE_CORRUPTIONS_STR + repairable_corruptions_string)

        if len(self.fatal_corruptions) > 0:
            fatal_corruptions_string: str = self.SEPARATOR.join([str(row) for row in self.fatal_corruptions])
            returned_inaccuracies.append(self.FATAL_CORRUPTIONS_STR + fatal_corruptions_string)

        return returned_inaccuracies

    def trim_data_set(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        trims the data set to the first trajectory entry for each sequence of the seg_type.
        :param data: the fcd ui dataframe
        :return: the trimmed dataframe
        """
        # only take the first trajectory entry from the seg_type column for each sequence.
        data['unique_entry'] = data[FcdColumn.TRIP.value].astype(str) \
                               + data[FcdColumn.DATE_TIME.value].astype(str)
        result: pd.DataFrame = data[data['seg_type'] == "trajectory"].groupby('unique_entry').first()
        result = result.reset_index(drop=True)
        return result
