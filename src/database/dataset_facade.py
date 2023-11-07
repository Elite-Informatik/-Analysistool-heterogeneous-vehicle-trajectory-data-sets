from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.record import DataRecord
from src.data_transfer.record.data_set_record import DatasetRecord
from src.model.error_handler import ErrorHandler


class DatasetFacade(ErrorHandler):
    """
    DatasetFacade is Interface for accessing Datasets in the Database.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_data_sets_as_dict(self) -> Dict[str, int]:
        """
        Getter for a dict of loaded data sets
        :return: Dataset metadata as a dict {name: size}
        """
        pass

    @abstractmethod
    def get_all_dataset_ids(self) -> List[UUID]:
        """
        Setter for all datasets that are already in the system
        """
        pass

    @abstractmethod
    def set_connection(self, connection: Dict[str, str]) -> bool:
        """
        Setter for the connection to the database.
        :param connection: A dictionary with the connection parameters of the database.
        :return: If the connection was established successfully.
        """
        pass

    @abstractmethod
    def get_data_set_meta(self, dataset_uuid: UUID) -> Optional[DatasetRecord]:
        """
        Getter for metadata of a dataset.
        :param dataset_uuid: The uuid of the dataset.
        :return: Dataset record of the dataset.
        """
        pass

    @abstractmethod
    def delete_dataset(self, dataset_uuid: UUID) -> bool:
        """
        Deletes a data set.
        :param dataset_uuid: UUID of the data set to delete.
        :return: Boolean indicating success of deletion.
        """
        pass

    @abstractmethod
    def add_dataset(self, data: DataRecord, append: bool = False) -> Optional[UUID]:
        """
        Adds a new data set.
        :param data: DataRecord object with the data for the new set.
        :param append: Boolean indicating if the data should be appended to the current data set.
        :return: UUID of the newly added data set.
        """
        pass

    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the database.
        :param table_name: Name of the table.
        :return: Boolean indicating if the table exists.
        """
        pass

    @abstractmethod
    def load_dataset(self, dataset_uuid: UUID) -> bool:
        """
        The dataset with the given id will be added to the currently active datasets. If the dataset is already active
        nothing will happen. Active means that when data is requested it will be requested from all active datasets.
        :param dataset_uuid: UUID of the dataset to load.
        :return: Boolean indicating if the dataset was loaded successfully.
        """
        pass

    @abstractmethod
    def unload_dataset(self, dataset_uuid: UUID) -> bool:
        """
        The dataset with the given id will be removed from the currently active datasets. If the dataset is not active
        nothing will happen.
        :param dataset_uuid: UUID of the dataset to unload.
        :return: Boolean indicating if the dataset was unloaded successfully.
        """

        pass

    @abstractmethod
    def get_active_datasets(self) -> List[UUID]:
        """
        Returns a list of the currently active datasets.
        :return: List of UUIDs of the currently active datasets.
        """
        pass
