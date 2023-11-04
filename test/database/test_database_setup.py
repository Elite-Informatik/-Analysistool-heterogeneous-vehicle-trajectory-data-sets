from unittest import TestCase
from unittest.mock import Mock

from uuid import uuid4

from src.database.database import Database
from src.database.dataset_meta_table import META_TABLE_COLUMNS, DatasetMetaTable


class AbstractTestDatabase(TestCase):
    def setUp(self) -> None:
        """
        Sets up the test by creating a mock database connection. In order to successfully mock the connection the
        classes that are called inside the sql library also have to be mocked.
        """
        self.mock_connection = Mock()
        self.mock_sql_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_engine = Mock()

        self.mock_connection.get_connection.return_value = self.mock_sql_connection
        self.mock_engine.cursor.return_value = self.mock_cursor
        self.mock_sql_connection.cursor.return_value = self.mock_cursor
        self.mock_sql_connection.engine = self.mock_engine

        self.dataset_id = uuid4()
        self.other_dataset_id = uuid4()
        self.dataset_size = 10

        # The description is the columns that will be returned by the
        self.mock_cursor.description = [[column] for column in META_TABLE_COLUMNS]
        self.mock_cursor.fetchall.return_value = [("test_dataset", self.dataset_id, self.dataset_size),
                                                  ("other_dataset", self.other_dataset_id, 20)]

        self.mock_connection.meta_table = "meta_table"
        self.mock_connection.data_table = "data_table"
        self.dataset_meta_table = DatasetMetaTable(self.mock_connection)


