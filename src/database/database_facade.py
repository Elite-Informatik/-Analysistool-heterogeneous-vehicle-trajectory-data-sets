from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.content import Column
from src.data_transfer.record.data_record import DataRecord
from src.data_transfer.record.data_set_record import DatasetRecord
from src.database.data_facade import DataFacade
from src.database.dataset_facade import DatasetFacade
from src.database.postgre_sql_data_facade import PostgreSQLDataFacade
from src.database.postgre_sql_dataset_facade import PostgreSQLDatasetFacade


class DatabaseFacade(DatasetFacade, DataFacade):
    """
    represents the facade of the database
    """

    def __init__(self):
        """
        Constructor for the database facade
        """
        super().__init__()
        self.data_facade = PostgreSQLDataFacade()
        self.dataset_facade = PostgreSQLDatasetFacade(self.data_facade)
        self.add_error_handler(self.data_facade)
        self.add_error_handler(self.dataset_facade)

    def get_data_sets_as_dict(self) -> Dict[str, int]:
        return self.dataset_facade.get_data_sets_as_dict()

    def set_data_sets_as_dict(self):
        return self.dataset_facade.set_data_sets_as_dict()

    def set_trajectory_filter(self, filter_str: str, use_filter: bool) -> None:
        self.data_facade.set_trajectory_filter(filter_str, use_filter)

    def set_point_filter(self, filter_str: str, use_filter: bool, negate_filter: bool) -> None:
        self.data_facade.set_point_filter(filter_str, use_filter, negate_filter)

    def set_connection(self, connection: Dict[str, str]) -> bool:
        return self.dataset_facade.set_connection(connection)

    def get_data_set_meta(self, dataset_uuid: UUID) -> Optional[DatasetRecord]:
        return self.dataset_facade.get_data_set_meta(dataset_uuid)

    def delete_dataset(self, dataset_uuid: UUID) -> bool:
        return self.dataset_facade.delete_dataset(dataset_uuid)

    def set_current_dataset(self, dataset_uuid: UUID) -> bool:
        return self.dataset_facade.set_current_dataset(dataset_uuid)

    def add_dataset(self, data: DataRecord, append: bool = False) -> Optional[UUID]:
        return self.dataset_facade.add_dataset(data, append)

    def get_data(self, returned_columns: List[Column]) -> Optional[DataRecord]:
        return self.data_facade.get_data(returned_columns)

    def get_distinct_data_from_column(self, returned_column: Column) -> Optional[DataRecord]:
        return self.data_facade.get_distinct_data_from_column(returned_column)

    def get_data_of_column_selection(self, returned_columns: List[Column], chosen_elements: List,
                                     chosen_column: Column, usefilter: bool = True) -> Optional[DataRecord]:
        return self.data_facade.get_data_of_column_selection(returned_columns, chosen_elements,
                                                             chosen_column, usefilter)

    def get_trajectory_ids(self) -> DataRecord:
        return self.data_facade.get_trajectory_ids()

    def table_exists(self, table_name: str) -> bool:
        return self.dataset_facade.table_exists(table_name)
