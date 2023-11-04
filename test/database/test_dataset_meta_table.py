from unittest import TestCase
from unittest.mock import Mock

from pandas import DataFrame
from uuid import uuid4, UUID

from sqlalchemy.exc import SQLAlchemyError

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.database.dataset_meta_table import DatasetMetaTable, META_TABLE_COLUMNS, META_TABLE_NAME, META_TABLE_UUID, \
    META_TABLE_SIZE
from src.database.sql_querys import SQLQueries
from test.database.test_database_setup import AbstractTestDatabase


class DatasetMetaTableTest(AbstractTestDatabase):
    """
    Tests the DatasetMetaTable class using mocks
    """

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
        new_instance = DatasetMetaTable(self.mock_connection)
        self.assertTrue(new_instance._table_exists)

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

    def test_get_all_datasets(self):
        """
        Tests if the test_get_all_datasets method works if no errors happen.
        """
        # It should raise an exception at first as more columns are returned then queried due to the way the initial
        # mock is set up.
        self.assertRaises(RuntimeError, self.dataset_meta_table.get_all_datasets)
        self.mock_cursor.description = [[META_TABLE_COLUMNS[1]]]
        ids = [uuid4() for _ in range(10)]
        self.mock_cursor.fetchall.return_value = [(dataset_id,) for dataset_id in ids]
        result = self.dataset_meta_table.get_all_datasets()
        self.assertListEqual(ids, result)

    def test_add_table(self):
        """
        Tests if adding of datasets to the meta table inside the database works correctly by checking if the correct
        sql query was executed.
        """
        dataset_name: str = "test"
        dataset_uuid: UUID = uuid4()
        dataset_size: int = 10

        self.dataset_meta_table.add_table(dataset_name=dataset_name, dataset_uuid=dataset_uuid,
                                          dataset_size=dataset_size)

        # Assert that the correct sql query was executed.
        expected_sql_query = f'INSERT INTO "meta_table" ' + (f'{tuple(META_TABLE_COLUMNS)}'.replace("\'", '"')
                                                             .replace(" ", "")) + ' VALUES (?,?,?)'

        self.mock_cursor.executemany.assert_called_with(expected_sql_query,
                                                        [(dataset_name, dataset_uuid, dataset_size)])

    def test_remove_dataset(self):
        """
        Tests if deleting of datasets from the meta table inside the database works correctly by checking if the
        correct sql query was executed.
        """
        dataset_uuid: UUID = uuid4()

        self.dataset_meta_table.remove_dataset(dataset_uuid=dataset_uuid)
        self.assertListEqual(self.dataset_meta_table.get_errors(), [])

        # Assert that the correct sql query was executed.
        expected_sql_query = SQLQueries.DELETE_DATASET.value.format(table_name=self.dataset_meta_table.name,
                                                                    column=META_TABLE_COLUMNS[1],
                                                                    uuid=dataset_uuid)

        self.mock_sql_connection.execute.assert_called_with(expected_sql_query)

    def test_contains(self):
        """
        Tests if the contains method works correctly.
        """
        # Mock the get_meta_data method to return a dummy dataframe
        self.dataset_meta_table.get_meta_data = Mock(return_value=DataFrame())
        # Call the contains method and assert that it returns True
        self.assertTrue(self.dataset_meta_table.contains(dataset_uuid=uuid4()))

    def test_adjust_size(self):
        """
        Tests if the increase size method calls the correct sql query.
        """
        new_size: int = 42
        adjusted: bool = self.dataset_meta_table.adjust_size(dataset_uuid=self.dataset_id, new_size=new_size)
        expected_sql_query = f"UPDATE '{self.mock_connection.meta_table}' SET {META_TABLE_COLUMNS[META_TABLE_SIZE]} = " \
                             f"{new_size} WHERE {META_TABLE_COLUMNS[META_TABLE_UUID]} = '{self.dataset_id}'"
        self.mock_sql_connection.execute.assert_called_with(expected_sql_query)
        self.assertTrue(adjusted)

    def test_adjust_size_error(self):
        """
        Tests if the increase size method returns False if an error occurs.
        """
        self.mock_sql_connection.execute.side_effect = SQLAlchemyError("error")
        # Call the increase_size method and assert that it returns False
        call_result: bool = self.dataset_meta_table.adjust_size(dataset_uuid=self.dataset_id, new_size=42)
        self.assert_size_errors(call_result, first_error=ErrorMessage.DATABASE_QUERY_ERROR)

    def assert_size_errors(self, call_result, first_error: ErrorMessage):
        """
        Helper method to assert that the correct errors are thrown when the size is not updated.
        """
        self.assertFalse(call_result)
        result_errors = [error.error_type for error in self.dataset_meta_table.get_errors()]
        self.assertTrue(first_error in result_errors)
        self.assertTrue(ErrorMessage.DATASET_SIZE_NOT_UPDATED in result_errors)

    def test_increase_size_error(self):
        """
        Tests if the increase size method returns False if an error occurs.
        """
        self.mock_sql_connection.execute.side_effect = SQLAlchemyError("error")
        self.mock_cursor.fetchall.return_value = []
        # Call the increase_size method and assert that it returns False
        call_result: bool = self.dataset_meta_table.increase_size(dataset_uuid=self.dataset_id, size_increase=42)
        self.assert_size_errors(call_result, first_error=ErrorMessage.DATASET_NOT_EXISTING)

    def test_increase_size(self):
        """
        Tests if the increase size method calls the correct sql query.
        """
        increase_size: int = 42
        self.mock_cursor.fetchall.return_value = [("test_dataset", self.dataset_id, 10)]
        adjusted: bool = self.dataset_meta_table.increase_size(dataset_uuid=self.dataset_id,
                                                               size_increase=increase_size)
        expected_sql_query = f"UPDATE '{self.mock_connection.meta_table}' " \
                             f"SET {META_TABLE_COLUMNS[META_TABLE_SIZE]} = " \
                             f"{self.dataset_size + increase_size} " \
                             f"WHERE {META_TABLE_COLUMNS[META_TABLE_UUID]} = '{self.dataset_id}'"
        self.mock_sql_connection.execute.assert_called_with(expected_sql_query)
        self.assertTrue(adjusted)

    def test_get_size(self):
        """
        Tests if the get_size method returns the correct size.
        """
        self.mock_cursor.fetchall.return_value = [("test_dataset", self.dataset_id, self.dataset_size)]
        size: int = self.dataset_meta_table.get_size(dataset_uuid=self.dataset_id)
        self.assertEqual(self.dataset_size, size)
