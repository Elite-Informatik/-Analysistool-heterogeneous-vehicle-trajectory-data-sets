from abc import ABC
from typing import List, Optional, Dict
from uuid import UUID

from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord, DatasetRecord
from src.database.data_facade import DataFacade
from src.database.database_facade import DatabaseFacade
from src.database.dataset_facade import DatasetFacade
from src.database.idatabase import IDatabase


class Database(IDatabase, DatasetFacade, DataFacade):
    """
    this interface represents a database
    """

    def get_data_sets_as_dict(self) -> Dict[str, int]:
        # todo: continue here
        pass

    def set_data_sets_as_dict(self) -> List[UUID]:
        pass

    def set_connection(self, connection: Dict[str, str]) -> bool:
        pass

    def get_data_set_meta(self, dataset_uuid: UUID) -> Optional[DatasetRecord]:
        pass

    def delete_dataset(self, dataset_uuid: UUID) -> bool:
        pass

    def set_current_dataset(self, dataset_uuid: UUID) -> bool:
        pass

    def add_dataset(self, data: DataRecord, append: bool = False) -> Optional[UUID]:
        pass

    def table_exists(self, table_name: str) -> bool:
        pass

    def set_point_filter(self, filter_str: str, use_filter: bool, negate_filter: bool) -> None:
        pass

    def set_trajectory_filter(self, filter_str: str, use_filter: bool) -> None:
        pass

    def get_data(self, returned_columns: List[Column]) -> DataRecord:
        pass

    def get_distinct_data_from_column(self, returned_column: Column) -> DataRecord:
        pass

    def get_data_of_column_selection(self, columns: List[Column], filter_elements: List, filter_column: Column,
                                     use_filter: bool = True) -> Optional[DataRecord]:
        pass

    def get_trajectory_ids(self) -> DataRecord:
        pass

    def __init__(self):
        super().__init__()

    @property
    def database_facade(self) -> "Database":
        """
        Returns the database facade
        """
        return self
