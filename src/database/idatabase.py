from abc import ABC
from abc import abstractmethod

from src.database.data_facade import DataFacade
from src.database.dataset_facade import DatasetFacade


class IDatabase(ABC):
    """
    this interface represents a database
    """

    @property
    @abstractmethod
    def dataset_facade(self) -> DatasetFacade:
        """
        the dataset facade
        """
        pass

    @property
    @abstractmethod
    def data_facade(self) -> DataFacade:
        """
        the dataset facade
        """
        pass
