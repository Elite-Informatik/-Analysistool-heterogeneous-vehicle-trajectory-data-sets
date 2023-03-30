from src.database.database_facade import DatabaseFacade
from src.database.idatabase import IDatabase


class Database(IDatabase):
    """
    this interface represents a database
    """

    def __init__(self):
        self._database_facade = DatabaseFacade()

    @property
    def database_facade(self) -> DatabaseFacade:
        """
        Returns the database facade
        """
        return self._database_facade
