import unittest
from unittest import mock
from unittest.mock import Mock

from pandas import DataFrame
from uuid import UUID, uuid4

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.data_transfer.record import DatasetRecord, DataRecord
from src.database import dataset
from src.database.data_provider import DataProvider
from src.database.database_connection import DatabaseConnection
from src.database.dataset import Dataset
from src.database.dataset_meta_table import META_TABLE_COLUMNS
from test.database.test_database import TestDatabase


class TestDataset(TestDatabase):

    def setUp(self):
        """
        Sets up the dataset tests by creating an example dataset.
        """
        super().setUp()

        self.dataset = Dataset(name="test_dataset", size=10, connection=self.mock_connection,
                               meta_table=self.dataset_meta_table, uuid=self.dataset_id)
        # Create a Dataset instance with a mock connection and some dummy attributes

    def test_to_dataset_record(self):
        # Test the to_dataset_record method
        # Call the method and get the result
        result = self.dataset.to_dataset_record()
        # Assert that the result is a DatasetRecord instance with the same name and size as the dataset
        self.assertIsInstance(result, DatasetRecord)
        self.assertEqual(result.name, self.dataset._name)
        self.assertEqual(result.size, self.dataset._size)

    def test_add_data_success(self):
        # Test the add_data method when the data is successfully added to the database
        # Mock the _get_connection method to return a dummy connection object
        self.dataset.get_connection = Mock(return_value="connection")
        # Mock the to_sql method of the dataframe object to return None
        mock_dataframe = Mock(spec=DataFrame)
        mock_dataframe.__setitem__ = Mock()
        # Create a DataRecord instance with some dummy data and column names
        data_record = DataRecord(_data=mock_dataframe, _column_names=("col1", "col2"), _name="test")
        # Call the method and get the result
        result = self.dataset.add_data(data_record)
        # Assert that the result is True and that the to_sql method was called with the expected arguments
        self.assertTrue(result)
        mock_dataframe.to_sql.assert_called_with(name=self.dataset._name, con="connection", if_exists="append",
                                                 index=False)

    def test_get_data_provider(self):
        """
        Tests if the get_data_provider method works correctly.
        """
        # Call the method and get the result
        result: DataProvider = self.dataset.get_data_provider()
        # Assert that the result is a DataProvider instance with the expected attributes
        self.assertIsInstance(result, DataProvider)
        self.assertEqual(result.dataset_uuids, [self.dataset._uuid])
        self.assertEqual(result.database_connection, self.mock_connection)

    def test_add_data_failure(self):
        # Test the add_data method when an error occurs while getting the connection or executing the query
        # Mock the _get_connection method to return None
        self.dataset.get_connection = Mock(return_value=None)
        # Create a DataRecord instance with some dummy data and column names
        mock_dataframe = mock.Mock(spec=DataFrame)
        data_record = DataRecord(_data=mock_dataframe, _column_names=("col1", "col2"), _name="test")
        # Call the method and get the result
        result = self.dataset.add_data(data_record)
        # Assert that the result is False and that the to_sql method was not called
        self.assertFalse(result)
        mock_dataframe.to_sql.assert_not_called()

    def test_load_from_database_success(self):
        self.mock_cursor.fetchall.return_value = [("test_dataset", self.dataset_id, 10)]
        result = Dataset.load_from_database(database_connection=self.mock_connection,
                                            meta_table=self.dataset_meta_table, uuid=self.dataset.uuid)
        # Assert that the result is a Dataset instance with the same attributes as the dataset
        self.assertIsInstance(obj=result, cls=Dataset)
        self.assertEqual(result._name, self.dataset.name)
        self.assertEqual(result._size, self.dataset.size)
        self.assertEqual(result._uuid, self.dataset.uuid)
        self.assertEqual(result.database_connection, self.dataset.database_connection)
        self.assertEqual(result.data_table_name, self.dataset.data_table_name)

    def test_load_from_database_failure(self):
        self.mock_connection.get_connection.side_effect = DatabaseConnectionError("error")
        # Create a random uuid
        random_uuid = uuid4()
        # Call the class method with the mock connection and the random uuid and get the result
        result = Dataset.load_from_database(database_connection=self.mock_connection,
                                            meta_table=self.dataset_meta_table, uuid=random_uuid)
        # Assert that the result is None
        # print([(record.error_type, record.args) for record in result.get_errors()])
        errors = [record.error_type for record in result.get_errors()]

        self.assertTrue(ErrorMessage.DATABASE_CONNECTION_ERROR in errors)
        self.assertTrue(ErrorMessage.DATASET_LOAD_ERROR in errors)
        # todo: make error lists into a set

    def test_load_from_database_random_uuid(self):
        """
        Tests rather the correct errors are thrown when a non-existent dataset is attempted to be loaded in.
        """
        self.mock_cursor.fetchall.return_value = []
        random_uuid = uuid4()
        result = Dataset.load_from_database(database_connection=self.mock_connection,
                                            meta_table=self.dataset_meta_table, uuid=random_uuid)

        expected_errors = {ErrorMessage.DATASET_LOAD_ERROR, ErrorMessage.DATASET_NOT_EXISTING}
        result_errors = result.get_errors()

        self.assertSetEqual(expected_errors, set([record.error_type for record in result_errors]))

        for record in result_errors:
            self.assertTrue(str(random_uuid) in record.args)

    def test_create_meta_entry_when_created(self):
        """
        Tests if an entry in the meta table is created when a dataset is created.
        """
        self.dataset_meta_table.add_table = Mock(return_value=True)
        dataset = Dataset(name="test_dataset", size=10, connection=self.mock_connection,
                          meta_table=self.dataset_meta_table, uuid="id1")
        self.dataset_meta_table.add_table.assert_called_with(dataset_name=dataset.name, dataset_uuid=dataset.uuid,
                                                             dataset_size=dataset.size)

    def test_delete_dataset(self):
        """
        Tests if the delete_dataset method works correctly.
        """
        # Mock the _get_connection method to return a dummy connection object
        self.dataset.get_connection = Mock(return_value="connection")
        # Mock the query_sql method to return a dummy dataframe mock the meta_table
        self.dataset.query_sql = Mock(return_value=DataFrame())
        self.dataset.meta_table = Mock()
        # Call the method and get the result
        result = self.dataset.delete_dataset()
        # Assert that the result is True and that the query_sql method was called with the expected arguments
        self.assertTrue(result)
        self.dataset.query_sql.assert_called_with(sql_query=dataset.SQLQueries.DELETE_DATASET.value.format(
            table_name=self.dataset.data_table_name, column=dataset.UUID_COLUMN_NAME, uuid=self.dataset._uuid),
            connection="connection", read=False
        )
        self.dataset.meta_table.remove_dataset.assert_called_with(dataset_uuid=self.dataset._uuid)
