from unittest import TestCase
from unittest.mock import Mock

from pandas import DataFrame

from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.database.dataset_meta_table import DatasetMetaTable


class DatasetMetaTableTest(TestCase):
    """
    Tests the DatasetMetaTable class using mocks
    """

    def setUp(self) -> None:
        """
        Sets up the test by creating a mock database connection.
        """
        self.mock_connection = Mock()
        mock_sql_connection = Mock()
        mock_cursor = Mock()

        self.mock_connection.get_connection.return_value = mock_sql_connection
        mock_sql_connection.cursor.return_value = mock_cursor
        mock_cursor.description = ["table_name"]
        mock_cursor.fetchall.return_value = [("meta_table",)]

        self.mock_connection.meta_table = "meta_table"
        self.dataset_meta_table = DatasetMetaTable(self.mock_connection)

    def test_exits_true(self):
        """
        Tests if the _exists method returns True if the table exists.
        """
        # Mock the query_sql method to return a dataframe with the table name
        self.dataset_meta_table.query_sql = Mock(return_value=DataFrame({"table_name": ["meta_table"]}))
        # Call the _exists method and assert that it returns True
        self.assertTrue(self.dataset_meta_table._exists())

    def test_exits_false(self):
        """
        Tests if the _exists method returns False if the table doesn't exist.
        """
        # Mock the query_sql method to return an empty dataframe
        self.dataset_meta_table.query_sql = Mock(return_value=DataFrame())
        # Call the _exists method and assert that it returns False
        self.assertFalse(self.dataset_meta_table._exists())

        self.dataset_meta_table.query_sql = Mock(return_value=DataFrame({"table_name": ["other_table"]}))
        self.assertFalse(self.dataset_meta_table._exists())

        self.dataset_meta_table.query_sql = Mock(return_value=DataFrame({"table_name": ["other_table", "another_table"],
                                                                         "table_schema": ["public", "public"],
                                                                         "table_type": ["BASE TABLE", "BASE TABLE"]}))
        self.assertFalse(self.dataset_meta_table._exists())

    def test_exists_error(self):
        """
        Tests if the _exists method returns False if an error occurs.
        """
        self.mock_connection.get_connection.side_effect = DatabaseConnectionError("error")
        # Call the _exists method and assert that it returns False
        self.assertFalse(self.dataset_meta_table._exists())

    def test_exists_static_true(self):
        """
        Tests if the _exists method returns True if the table exists but a new instance of the class is created.
        """
        # Mock the query_sql method to return a dataframe with the table name
        self.dataset_meta_table.query_sql = Mock(return_value=DataFrame({"table_name": ["meta_table"]}))
        # Call the _exists method and assert that it returns True
        self.assertTrue(DatasetMetaTable(self.mock_connection)._exists())

    def test_create_table_success(self):
        """
        Tests if the _create_table method returns True if the table was created successfully.
        """
        # Mock the query_sql method on the DatasetMetaTable instance to return None
        self.dataset_meta_table.query_sql = Mock(return_value=None)
        # Call the create_table method and assert that it returns True
        self.assertTrue(self.dataset_meta_table._create_table())

    def test_create_table_error(self):
        """
        Tests if the _create_table method returns False if an error occurs.
        """
        self.mock_connection.get_connection.side_effect = DatabaseConnectionError("error")
        # Call the create_table method and assert that it returns False
        self.assertFalse(self.dataset_meta_table._create_table())
