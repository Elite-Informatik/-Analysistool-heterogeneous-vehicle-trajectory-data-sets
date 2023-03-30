from abc import ABC
from abc import abstractmethod

from src.database.database_facade import DatabaseFacade


class IDatabase(ABC):
    """
    this interface represents a database
    """

    @property
    @abstractmethod
    def database_facade(self) -> DatabaseFacade:
        """
        the database facade
        """
        pass
