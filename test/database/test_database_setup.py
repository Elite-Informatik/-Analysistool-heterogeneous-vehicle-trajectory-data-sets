from unittest import TestCase
from unittest.mock import Mock

from uuid import uuid4

from src.database.database import Database
from src.database.dataset_meta_table import META_TABLE_COLUMNS, DatasetMetaTable, META_TABLE_UUID


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

        # The description is the columns that will be returned by the cursor. The fetchall method returns a list of
        # tuples. Each tuple represents a row in the database. The first tuple is the first row, the second tuple is
        # the second row and so on. It is firstly set to one column because the meta table checks on startup for
        # validity and expects only one column.
        self.mock_cursor.description = [[META_TABLE_COLUMNS[META_TABLE_UUID]]]
        self.mock_cursor.fetchall.return_value = [(str(self.dataset_id),),
                                                  (str(self.other_dataset_id),)]

        self.mock_connection.meta_table = "meta_table"
        self.mock_connection.data_table = "data_table"
        self.dataset_meta_table = DatasetMetaTable(self.mock_connection)
        self.mock_cursor.description = [[column] for column in META_TABLE_COLUMNS]
        self.mock_cursor.fetchall.return_value = [("test_dataset", self.dataset_id, self.dataset_size),
                                                  ("other_dataset", self.other_dataset_id, 20)]

    def test_setup(self):
        """
        Tests if the setup was successful by checking if the mock connection is returned by the database.
        """


