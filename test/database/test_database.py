from uuid import UUID

from pandas import DataFrame

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.record import DataRecord
from test.database.test_database_setup import AbstractTestDatabase
from src.database.database import Database, REQUIRED_CONNECTION_KEYS, HOST, USER, PASSWORD, DATABASE, PORT, DATA_TABLE, \
    META_TABLE


class TestDatabase(AbstractTestDatabase):
    """
    This class tests the Database class in the database module.
    """

    def setUp(self) -> None:
        """
        Sets up the test by creating a mock database connection. In order to successfully mock the connection the
        classes that are called inside the sql library also have to be mocked.
        """
        super().setUp()
        self.database = Database()
        self.database.connection = self.mock_connection
        self.database.meta_table = self.dataset_meta_table
        self.mock_cursor.fetchall.return_value = [("test_dataset", self.dataset_id, self.dataset_size)]

    def test_set_connection_key_error(self):
        """
        Tests if the set_connection method sets the connection correctly.
        """
        connection = {}

        self.assertRaises(KeyError, self.database.set_connection, connection)

    def test_set_connection_error_setting(self):
        """
        Tests if the set_connection method throws an error when wrong keys are used.
        """
        connection = {REQUIRED_CONNECTION_KEYS[HOST]: "not_host",
                      REQUIRED_CONNECTION_KEYS[USER]: "not_user",
                      REQUIRED_CONNECTION_KEYS[PASSWORD]: "random_password",
                      REQUIRED_CONNECTION_KEYS[DATABASE]: "database",
                      REQUIRED_CONNECTION_KEYS[PORT]: 123,
                      REQUIRED_CONNECTION_KEYS[DATA_TABLE]: "data_table",
                      REQUIRED_CONNECTION_KEYS[META_TABLE]: "meta_table"}

        self.database.set_connection(connection)
        self.assertTrue(self.database.error_occurred())

    def test_load_dataset(self):
        """
        Tests if the load_dataset method loads the dataset correctly.
        """
        self.database.load_dataset(self.dataset_id)
        self.assertTrue(len(self.database._error_handlers) == 1)
        self.assertTrue(len(self.database.active_datasets) == 1)

    def test_load_dataset_error(self):
        """
        Tests if the load_dataset method throws an error when the dataset does not exist.
        """
        self.mock_cursor.fetchall.return_value = []
        result: bool = self.database.load_dataset(self.dataset_id)
        self.assertFalse(result)
        errors = self.database.get_errors()
        self.assertTrue(ErrorMessage.DATASET_LOAD_ERROR in [error.error_type for error in errors])
        self.assertTrue(len(self.database._error_handlers) == 0)
        self.assertTrue(len(self.database.active_datasets) == 0)

    def test_get_active_datasets(self):
        """
        Tests if the get_active_datasets method returns the correct datasets.
        """
        self.database.load_dataset("mock dataset will be returned, as defined in setUp")
        self.assertTrue(self.dataset_id in self.database.get_active_datasets())

    def test_delete_dataset(self):
        """
        Tests if the delete_dataset method deletes the dataset correctly.
        """
        self.database.load_dataset(self.dataset_id)
        self.database.delete_dataset(self.dataset_id)
        self.assertTrue(len(self.database._error_handlers) == 0)
        self.assertTrue(len(self.database.active_datasets) == 0)

    def test_delete_dataset_not_loaded(self):
        """
        Tests if the delete_dataset method does not throw an error when the dataset is not loaded.
        """
        self.database.delete_dataset(self.dataset_id)
        self.assertTrue(len(self.database._error_handlers) == 0)
        self.assertTrue(len(self.database.active_datasets) == 0)
        errors = self.database.get_errors()
        # no error should occur as the dataset is not loaded but still exists in the "database"
        self.assertTrue(len(errors) == 0)

    def test_delete_dataset_error(self):
        """
        Tests if the delete_dataset method throws an error when the dataset does not exist.
        """
        self.mock_cursor.fetchall.return_value = []

        self.assertRaises(RuntimeError, self.database.delete_dataset, self.dataset_id)

    def test_add_dataset(self):
        """
        Tests if the add_dataset method adds the dataset correctly.
        """
        data_records: DataRecord = DataRecord(
            _name="test_dataset",
            _column_names = ("test_column"),
            _data=DataFrame(data={"test_column": [1, 2, 3]}))
        result = self.database.add_dataset(data_records)
        # this should in theory fail but there is no way to check weather the pandas to sql operation was
        # successful or not.
        self.assertIsInstance(result, UUID)

    def test_unload_dataset(self):
        """
        Tests if the unload_dataset method unloads the dataset correctly.
        """
        self.database.load_dataset(self.dataset_id)
        self.database.unload_dataset(self.dataset_id)
        self.assertTrue(len(self.database._error_handlers) == 0)
        self.assertTrue(len(self.database.active_datasets) == 0)
