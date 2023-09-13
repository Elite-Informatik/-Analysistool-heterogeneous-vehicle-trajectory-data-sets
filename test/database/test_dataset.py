import unittest
from unittest import mock
from unittest.mock import Mock

from pandas import DataFrame
from uuid import UUID, uuid4

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.data_transfer.record import DatasetRecord, DataRecord
from src.database import dataset
from src.database.database_connection import DatabaseConnection
from src.database.dataset import Dataset
from src.database.dataset_meta_table import META_TABLE_COLUMNS


class TestDataset(unittest.TestCase):

    def setUp(self):
        # Create a mock connection object
        self.mock_connection = Mock(spec=DatabaseConnection)
        # Set the meta_table and data_table attributes to dummy names
        self.mock_connection.meta_table = "meta_table"
        self.mock_connection.data_table = "data_table"

        self.mock_sql_connection = Mock()
        self.mock_cursor = Mock()

        self.mock_connection.get_connection.return_value = self.mock_sql_connection
        self.mock_sql_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.description = [[column] for column in META_TABLE_COLUMNS]
        self.mock_cursor.fetchall.return_value = [("test_dataset", "id1", 10)]

        self.dataset = Dataset(name="test_dataset", size=10, connection=self.mock_connection, uuid="id1")
        # Create a Dataset instance with a mock connection and some dummy attributes

    def test_to_dataset_record(self):
        # Test the to_dataset_record method
        # Call the method and get the result
        result = self.dataset.to_dataset_record()
        # Assert that the result is a DatasetRecord instance with the same name and size as the dataset
        self.assertIsInstance(result, DatasetRecord)
        self.assertEqual(result.name, self.dataset._name)
        self.assertEqual(result.size, self.dataset._size)

    def test_get_data_success(self):
        # Test the get_data method when the data is successfully retrieved from the database
        # Mock the _get_connection method to return a dummy connection object
        self.dataset._get_connection = Mock(return_value="connection")
        # Mock the query_sql method to return a dataframe with some dummy data and a uuid column
        mock_data = DataFrame(
            {"col1": [1, 2, 3], "col2": ["a", "b", "c"], dataset.UUID_COLUMN_NAME: [self.dataset._uuid] * 3})
        self.dataset.query_sql = Mock(return_value=mock_data)
        # Call the method and get the result
        result = self.dataset.get_data()
        # Assert that the result is a DataRecord instance with the same name as the dataset and the expected data and column names
        self.assertIsInstance(result, DataRecord)
        self.assertEqual(result._name, self.dataset._name)
        expected_data = DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        expected_columns = ["col1", "col2"]
        self.assertTrue(result._data.equals(expected_data))
        self.assertEqual(list(result._column_names), expected_columns)

    def test_get_data_failure(self):
        # Test the get_data method when an error occurs while getting the connection or executing the query
        # Mock the _get_connection method to return None
        self.dataset._get_connection = mock.Mock(return_value=None)
        # Call the method and get the result
        result = self.dataset.get_data()
        # Assert that the result is a DataRecord instance with the same name as the dataset and an empty data and column names
        self.assertIsInstance(result, DataRecord)
        self.assertEqual(result._name, self.dataset._name)
        expected_data = DataFrame()
        expected_columns = []
        self.assertTrue(result._data.empty)
        self.assertEqual(list(result._column_names), expected_columns)

    def test_add_data_success(self):
        # Test the add_data method when the data is successfully added to the database
        # Mock the _get_connection method to return a dummy connection object
        self.dataset._get_connection = Mock(return_value="connection")
        # Mock the to_sql method of the dataframe object to return None
        mock_dataframe = Mock(spec=DataFrame)
        mock_dataframe.__setitem__ = Mock()
        mock_dataframe.to_sql.return_value = None
        # Create a DataRecord instance with some dummy data and column names
        data_record = DataRecord(_data=mock_dataframe, _column_names=("col1", "col2"), _name="test")
        # Call the method and get the result
        result = self.dataset.add_data(data_record)
        # Assert that the result is True and that the to_sql method was called with the expected arguments
        self.assertTrue(result)
        mock_dataframe.to_sql.assert_called_with(name=self.dataset._name, con="connection", if_exists="append",
                                                 index=False)

    def test_add_data_failure(self):
        # Test the add_data method when an error occurs while getting the connection or executing the query
        # Mock the _get_connection method to return None
        self.dataset._get_connection = Mock(return_value=None)
        # Create a DataRecord instance with some dummy data and column names
        mock_dataframe = mock.Mock(spec=DataFrame)
        data_record = DataRecord(_data=mock_dataframe, _column_names=("col1", "col2"), _name="test")
        # Call the method and get the result
        result = self.dataset.add_data(data_record)
        # Assert that the result is False and that the to_sql method was not called
        self.assertFalse(result)
        mock_dataframe.to_sql.assert_not_called()

    def test_load_from_database_success(self):

        result = Dataset.load_from_database(database_connection=self.mock_connection, uuid=self.dataset.uuid)
        # Assert that the result is a Dataset instance with the same attributes as the dataset
        self.assertIsInstance(obj=result, cls=Dataset)
        self.assertEqual(result._name, self.dataset.name)
        self.assertEqual(result._size, self.dataset.size)
        self.assertEqual(result._uuid, self.dataset.uuid)
        self.assertEqual(result.connection, self.dataset.connection)
        self.assertEqual(result.data_table_name, self.dataset.data_table_name)

    def test_load_from_database_failure(self):

        self.mock_connection.get_connection.side_effect = DatabaseConnectionError("error")
        # Create a random uuid
        random_uuid = uuid4()
        # Call the class method with the mock connection and the random uuid and get the result
        result = Dataset.load_from_database(database_connection=self.mock_connection, uuid=random_uuid)
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
        result = Dataset.load_from_database(database_connection=self.mock_connection, uuid=random_uuid)

        expected_errors = [ErrorMessage.DATASET_LOAD_ERROR, ErrorMessage.DATASET_NOT_EXISTING]

        self.assertListEqual(expected_errors, [record.error_type for record in result.get_errors()])

        for record in result.get_errors():
            self.assertTrue(str(random_uuid) in record.args)
