from typing import List, Dict, Tuple

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.content.data_types import DataTypes
from src.data_transfer.content.road_type import RoadType, VehicleType
from src.data_transfer.exception import ExecutionFlowError
from src.data_transfer.record import DataRecord
from src.file.converter.bicycle_simra.simra_bicycle_columns import SimraColumn
from src.file.converter.bicycle_simra.simra_bicycle_handler import IDCalculator, TrajectoryIDCalculator, DateCalculator, \
    TimeCalculator, LatitudeCalculator, LongitudeCalculator, ConstantConverter, SpeedCalculator, \
    AccelerationMagnitudeCalculator, AccelerationDirectionCalculator, SpeedDirectionCalculator
from src.file.converter.data_converter import DataConverter
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AbstractColumnCalculator

FORMAT: str = DataTypes.SIMRA.value


class SimraConverter(DataConverter):
    """
    This converter converts datasets of the SimRa project into the unified data format.
    """
    def __init__(self):
        self.verified = False
        self.handler_map: Dict[Column, AbstractColumnCalculator] = {
            Column.ID: IDCalculator(),
            Column.TRAJECTORY_ID: TrajectoryIDCalculator(),
            Column.DATE: DateCalculator(),
            Column.TIME: TimeCalculator(),
            Column.LATITUDE: LatitudeCalculator(),
            Column.LONGITUDE: LongitudeCalculator(),
            Column.SPEED: SpeedCalculator(),
            Column.SPEED_LIMIT: ConstantConverter(Column.SPEED_LIMIT, 0),
            Column.ACCELERATION: AccelerationMagnitudeCalculator(),
            Column.ACCELERATION_DIRECTION: AccelerationDirectionCalculator(),
            Column.SPEED_DIRECTION: SpeedDirectionCalculator(),
            Column.ROAD_TYPE: ConstantConverter(Column.ROAD_TYPE, RoadType.UNCLASSIFIED.value),
            Column.OSM_ROAD_ID: ConstantConverter(Column.OSM_ROAD_ID, 0),
            Column.ONE_WAY_STREET: ConstantConverter(Column.ONE_WAY_STREET, False),
            Column.VEHICLE_TYPE: ConstantConverter(Column.VEHICLE_TYPE, VehicleType.BICYCLE.value)
        }
        self.invalid_columns: List[Column] = []
        self.repairable_corruptions: List[Tuple[Column, List[int]]] = []
        self.fatal_corruptions: List[int] = []

    def is_convertable(self, data: List[DataRecord]) -> bool:
        self.verified = True
        convertable = True
        for column, handler in self.handler_map.items():
            for data_record in data:
                if not handler.is_repairable(data_record.data):
                    self.invalid_columns.append(column)
                    #self.fatal_corruptions.extend(handler.fatal_corruptions)
                    convertable = False

        return convertable

    def search_inaccuracies(self, data: List[DataRecord]) -> List[str]:
        inaccuracies: List[str] = []
        for data_record in data:
            for column, handler in self.handler_map.items():
                error_lines = handler.find_repairable_corruptions(data_record.data)
                if len(error_lines) == 0:
                    continue
                error_string = "Column:" + column.value + ", has errors in the lines: " \
                                 + str(error_lines)
                inaccuracies.append(error_string)
        return inaccuracies


    def convert_to_data(self, data: List[DataRecord]) -> DataRecord:
        """
        converts the given List of source data records of the simra bicycle data into a DataRecord.
        """
        if not self.verified:
            raise \
                ExecutionFlowError(f"The Dataset has not been validated by the {self.is_convertable.__name__} method.")
        destination_df: pd.DataFrame = pd.DataFrame()
        result_df: pd.DataFrame = pd.DataFrame()

        for data_record in data:
            source_df: pd.DataFrame = self.trim_data_set(data_record.data)
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

            result_df = pd.concat([result_df, destination_df], ignore_index=True, sort=False)

        return DataRecord("new fcd ui dataset", (), result_df)

    def get_data_format(self) -> str:
        return FORMAT

    def trim_data_set(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Deletes all the lines in which the latitude or longitude are not set
        """
        return data.dropna(subset=[SimraColumn.LATITUDE.value, SimraColumn.LONGITUDE.value]).reset_index(drop=True)

