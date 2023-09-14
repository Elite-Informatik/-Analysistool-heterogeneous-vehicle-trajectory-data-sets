from abc import ABC

from src.database.data_facade import DataFacade
from src.database.database_facade import DatabaseFacade
from src.database.dataset_facade import DatasetFacade
from src.database.idatabase import IDatabase


class Database(IDatabase, DatabaseFacade):
    """
    this interface represents a database
    """

    def __init__(self):
        super().__init__()


    @property
    def database_facade(self) -> DatabaseFacade:
        """
        Returns the database facade
        """
        return self
