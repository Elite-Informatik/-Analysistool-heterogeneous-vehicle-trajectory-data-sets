from typing import List

from src.data_transfer.content import Column
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseException
from src.data_transfer.record import DataRecord
from src.database.data_provider import DataProvider
from src.database.sql_querys import SQLQueries
from test.database.test_database import TestDatabase
from src.database.database_component import UUID_COLUMN_NAME


class DataProviderTest(TestDatabase):
    """
    Tests the DataProvider class using mocks.
    """

    def setUp(self) -> None:
        """
        Sets up the test by creating a mock database connection.
        """
        super().setUp()
        # Create a DataProvider instance with a mock connection and some dummy attributes
        self.data_provider = DataProvider(dataset_uuids=[self.dataset_id], connection=self.mock_connection)

    def test_set_point_filter(self):
        """
        Tests the set point filter method without the negation of the filter.
        """
        # Call the method with the given parameters
        filter_str: str = "filter"
        self.data_provider.set_point_filter(filter_str=filter_str, use_filter=True, negate_filter=False)
        # Assert that the filter was added to the filters list
        self.assertEqual(self.data_provider.point_filter, filter_str)

    def test_set_point_filter_negation(self):
        """
        Tests if the set point filter method works correctly when the filter is negated.
        """
        # Call the method with the given parameters
        filter_str: str = "filter"
        self.data_provider.set_point_filter(filter_str=filter_str, use_filter=True, negate_filter=True)
        # Assert that the filter was added to the filters list
        self.assertEqual(self.data_provider.point_filter, SQLQueries.NOT.value.format(filter=filter_str))

    def test_get_data_without_point_filter(self):
        """
        Tests if the get_data method works correctly when no point filter is set.
        """
        self._assert_query_and_data()

    def test_aget_data_with_point_filter(self):
        """
        Tests if the get_data method works correctly when a point filter is set.
        """
        self.data_provider.point_filter = "filter"
        self._assert_query_and_data(point_filter="filter")

    def _assert_query_and_data(self, point_filter: str = ""):
        """
        Helper method to assert the query and data returned by the data provider.
        """
        columns = [Column.LATITUDE, Column.LONGITUDE]
        result = self.data_provider.get_data(columns=columns)
        expected_query: str = f"SELECT {columns[0].value}, {columns[1].value} FROM {self.mock_connection.data_table} " \
                              f"WHERE {UUID_COLUMN_NAME} IN ({str(self.dataset_id)})"
        if point_filter != "":
            expected_query += f" AND {point_filter}"
        self._check_result(result=result, expected_query=expected_query)

    def test_set_trajectory_filter(self):
        """
        Tests the set trajectory filter method.
        """
        # Call the method with the given parameters
        filter_str: str = "filter"
        self.data_provider.set_trajectory_filter(filter_str=filter_str, use_filter=True)
        # Assert that the filter was added to the filters list
        self.assertEqual(self.data_provider.trajectory_filter, filter_str)

    def test_get_distinct_data_from_column(self):
        """
        Tests the get distinct data from column method.
        """
        # Call the method with the given parameters
        column: Column = Column.LATITUDE
        result = self.data_provider.get_distinct_data_from_column(column=column)
        # Assert that the correct query was called.
        expected_query: str = f"SELECT DISTINCT {column.value} FROM {self.mock_connection.data_table} " \
                              f"WHERE {UUID_COLUMN_NAME} IN ({str(self.dataset_id)})"
        self._check_result(result=result, expected_query=expected_query)

    def _check_result(self, result: DataRecord, expected_query: str):
        """
        Helper method to check the result of a query.
        """
        self.mock_cursor.execute.assert_called_with(expected_query)
        result_data = [tuple(series.to_list()) for (row, series) in result.data.iterrows()]
        self.assertIsNotNone(result_data)

        # The id of the datasets is not returned as it is not strictly part of the metadata.
        expected_data = [(name, size) for (name, _, size) in self.mock_cursor.fetchall()]
        self.assertListEqual(expected_data, result_data)
        self.assertIsInstance(result, DataRecord)

    def _helper_get_data_of_column_selection(self, point_filter: str = ""):
        """
        Tests the get data of column selection method.
        """
        # Call the method with the given parameters
        columns: List[Column] = [Column.LATITUDE, Column.LONGITUDE]
        filter_elements: List[str] = ["test_id1", "test_id2"]
        filter_column: Column = Column.TRAJECTORY_ID
        result = self.data_provider.get_data_of_column_selection(columns=columns, filter_elements=filter_elements,
                                                                 filter_column=filter_column, use_filter=True)
        # Assert that the correct query was called.
        expected_query: str = f"SELECT {columns[0].value}, {columns[1].value} FROM {self.mock_connection.data_table} " \
                              f"WHERE {UUID_COLUMN_NAME} IN ({str(self.dataset_id)}) AND " \
                              f"{filter_column.value} IN ({', '.join(filter_elements)})"
        if point_filter != "":
            expected_query += f" AND {point_filter}"
        self._check_result(result=result, expected_query=expected_query)

    def test_get_data_of_column_selection(self):
        """
        Tests the get data of column selection method without a point filter.
        """
        self._helper_get_data_of_column_selection()

    def test_get_data_of_column_selection_with_point_filter(self):
        """
        Tests the get data of column selection method with a point filter.
        """
        self.data_provider.point_filter = "filter"
        self._helper_get_data_of_column_selection(point_filter="filter")

    def test_get_trajectory_ids(self):
        """
        Tests the get trajectory ids method.
        """
        result = self.data_provider.get_trajectory_ids()
        trajectory_column: str = Column.TRAJECTORY_ID.value
        expected_query = f"SELECT DISTINCT {trajectory_column} FROM {self.mock_connection.data_table} " \
                         f"WHERE {UUID_COLUMN_NAME} IN ({str(self.dataset_id)})"
        self._check_result(result=result, expected_query=expected_query)

    def test_get_trajectory_ids_with_point_filter(self):
        """
        Tests the get trajectory ids method with a point filter.
        """
        trajectory_filter: str = "filter"
        self.data_provider.trajectory_filter = trajectory_filter
        self.data_provider.trajectory_filter_active = True
        result = self.data_provider.get_trajectory_ids()
        trajectory_column: str = Column.TRAJECTORY_ID.value
        expected_query = f"SELECT DISTINCT {trajectory_column} FROM {self.mock_connection.data_table} " \
                            f"WHERE {UUID_COLUMN_NAME} IN ({str(self.dataset_id)}) AND {trajectory_filter}"
        self._check_result(result=result, expected_query=expected_query)

    def test_assert_error_when_connection_is_none(self):
        """
        Asserts that an error is thrown when the connection is None.
        """
        self.mock_connection.get_connection.return_value = None
        data = self.data_provider._get_data_from_query("query")
        expected_errors = [ErrorMessage.DATASET_DATA_ERROR]
        actual_errors = [error.error_type for error in self.data_provider.get_errors()]
        self.assertListEqual(expected_errors, actual_errors)
        self.assertIsNone(data)

    def test_uuid_column_not_present(self):
        """
        Tests if the correct errors are thrown when the uuid column is not contained in the data
        the database returns.
        """
        columns: List[str] = ["name", "size"]
        self.mock_cursor.description = [[column] for column in columns]
        self.mock_cursor.fetchall.return_value = [("test_dataset", 10),
                                                  ("test_dataset2", 10)]
        try:
            self.data_provider._get_data_from_query("query")
            self.fail("Expected DatabaseException")
        except DatabaseException as e:
            self.assertIsInstance(e, DatabaseException)
            self.assertEqual(ErrorMessage.DATABASE_DATASET_UUID_MISSING_ERROR
                             .value.format(expected=UUID_COLUMN_NAME, got=columns), e.args[0])

