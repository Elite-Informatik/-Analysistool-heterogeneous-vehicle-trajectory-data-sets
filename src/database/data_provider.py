from typing import List, Optional

from uuid import UUID

from pandas import DataFrame
from sqlalchemy import Connection

from src.data_transfer.content import Column
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import InvalidInput
from src.data_transfer.exception.custom_exception import DatabaseException
from src.data_transfer.record import DataRecord
from src.database.data_facade import DataFacade
from src.database.database_component import DatabaseComponent, UUID_COLUMN_NAME
from src.database.database_connection import DatabaseConnection
from src.database.dataset_facade import DatasetFacade
from src.database.dataset_meta_table import DatasetMetaTable
from src.database.sql_querys import SQLQueries


class DataProvider(DatabaseComponent, DataFacade):
    """
    This class represents the data provider. It is created by a dataset to allow filtered access to the data.
    It filters the data according to the filter string set and filters the data in the database using sql.
    """

    def __init__(self):
        """
        Constructor for the data provider.
        :param dataset_uuids: A list of uuids of the datasets that should be used to get the data from.
        :param connection: The connection to the database as a DatabaseComponent.
        :param dataset_facade: The facade to the datasets so that the data provider can get the active datasets.
        """
        super().__init__(database_connection=None)
        self.point_filter: Optional[str] = None
        self.trajectory_filter: Optional[str] = None
        self.trajectory_filter_active: bool = False
        self.dataset_facade: Optional[DatasetFacade] = None
        self.meta_table: Optional[DatasetMetaTable] = None  # for future use of filtering by metadata

    def setParameters(self, connection: DatabaseConnection, dataset_facade: DatasetFacade,
                      meta_table: DatasetMetaTable):
        """
        Sets the parameters for the data provider. This is done this way and not in the constructor as on program start
        the data provider instance needs to be passed as the datafacade to the rest of the program. At that point the
        connection and the dataset facade are not yet available.
        """
        self.dataset_facade = dataset_facade
        self.meta_table = meta_table  # for future use of filtering by metadata
        self.database_connection = connection

    def set_point_filter(self, filter_str: str, use_filter: bool, negate_filter: bool) -> None:
        """
        Sets a point filter for the data points. The filter is a sql where clause that is used to filter the data
        later on when the data is requested.
        :param filter_str: String representation of the filter as a sql where clause.
        :param use_filter: Boolean indicating if the filter should be used.
        :param negate_filter: Boolean indicating if the filter should be negated.
        """
        if filter_str is None or filter_str == "":
            self.point_filter = None
            return

        self.point_filter = filter_str
        if negate_filter:
            self.point_filter = SQLQueries.NOT.value.format(filter=filter_str)

    def set_trajectory_filter(self, filter_str: str, use_filter: bool) -> None:
        """
        Sets a filter for the trajectories. The filter is a sql where clause that is used to filter the data
        later on when the trajectories are requested.
        :param filter_str: String representation of the filter as a sql where clause.
        :param use_filter: Boolean indicating if the filter should be applied when getting the list of trajectories.
        """
        if filter_str is None or filter_str == "":
            self.trajectory_filter = None
            return
        self.trajectory_filter = filter_str
        self.trajectory_filter_active = use_filter

    def get_data(self, columns: List[Column]) -> Optional[DataRecord]:
        """
        Gets the data with the specified columns. The data is filtered according to the filters set before.
        :param columns: List of Column objects specifying the columns to return. I.e. the columns the returned dataframe
        should have.
        :param dataset_uuids: List of uuids of the datasets to get the data from.
        :return: DataRecord object with the requested data.
        """
        dataset_uuids: List[UUID] = self._get_dataset_uuids()
        str_columns: List[str] = [column.value for column in columns]
        str_uuids: List[str] = ["'"+str(uuid)+"'" for uuid in dataset_uuids]

        query: str = SQLQueries.SELECT_FROM_DATASET.value.format(columns=", ".join(str_columns),
                                                                 tablename=self.database_connection.data_table,
                                                                 dataset_column=UUID_COLUMN_NAME,
                                                                 dataset_uuids=", ".join(str_uuids))

        if self.point_filter is not None:
            query += SQLQueries.AND.value.format(filter=self.point_filter)

        data = self._get_data_from_query(query)

        if data is None:
            return None

        return DataRecord(_data=data, _column_names=data.columns, _name=self.database_connection.data_table)

    def get_distinct_data_from_column(self, column: Column) -> Optional[DataRecord]:
        """
        Gets the unique values from the specified column. The previously set filters are not applied.
        :param column: Column object specifying the column to return the distinct data from.
        """
        dataset_uuids: List[UUID] = self._get_dataset_uuids()
        str_uuids: List[str] = ["'"+str(uuid)+"'" for uuid in dataset_uuids]
        query: str = SQLQueries.SELECT_DISTINCT_FROM_DATASET.value.format(columns=column.value,
                                                                          tablename=self.database_connection.data_table,
                                                                          dataset_column=UUID_COLUMN_NAME,
                                                                          dataset_uuids=", ".join(str_uuids))

        data = self._get_data_from_query(query)
        if data is None:
            return None
        return DataRecord(_name=column.value, _data=data, _column_names=(column.value,))

    def get_data_of_column_selection(self, columns: List[Column], filter_elements: List, filter_column: Column,
                                     use_filter: bool = True) -> Optional[DataRecord]:
        """
        Gets the data with the specified columns filtered by the filter elements in the filter column.
        E.g. if the filter column is the trajectory column and the filter elements are the uuids of the trajectories
        the returned dataframe will only contain data from the specified trajectories.
        :param columns: List of Column objects specifying the columns to return. I.e. the columns the returned dataframe
        should have.
        :param filter_elements: List of elements specifying the elements to filter by in the column.
        :param filter_column: Column object specifying the column to filter on.
        :param use_filter: Boolean indicating if the potentially previously defined filter should be applied when
        getting the data.
        :return: Optional DataRecord object with the requested data. Returns None if an error occurred.
        """

        dataset_uuids: List[UUID] = self._get_dataset_uuids()
        str_columns: List[str] = [column.value for column in columns]
        str_ids: List[str] = ["'"+str(uuid) + "'" for uuid in dataset_uuids]
        str_filter_elements: List[str] = ["'" + str(element) + "'" for element in filter_elements]

        query: str = SQLQueries.SELECT_FROM_DATASET.value.format(columns=", ".join(str_columns),
                                                                 tablename=self.database_connection.data_table,
                                                                 dataset_column=UUID_COLUMN_NAME,
                                                                 dataset_uuids=", ".join(str_ids))
        query += SQLQueries.AND_IN.value.format(column=filter_column.value,
                                                values=", ".join(str_filter_elements))

        if use_filter and self.point_filter is not None:
            query += SQLQueries.AND.value.format(filter=self.point_filter)

        data = self._get_data_from_query(query)
        if data is None:
            return None

        return DataRecord(_data=data, _column_names=data.columns, _name=self.database_connection.data_table)

    def get_trajectory_ids(self) -> Optional[DataRecord]:
        """
        Gets the ids of all unique trajectory ids in the selected datasets.
        :return: Optional DataRecord object with the requested data. Returns None if an error occurred.
        """
        dataset_uuids: List[UUID] = self._get_dataset_uuids()
        str_ids: List[str] = ["'"+str(uuid)+"'" for uuid in dataset_uuids]
        query: str = SQLQueries.SELECT_DISTINCT_FROM_DATASET.value.format(columns=Column.TRAJECTORY_ID.value,
                                                                          tablename=self.database_connection.data_table,
                                                                          dataset_column=UUID_COLUMN_NAME,
                                                                          dataset_uuids=", ".join(str_ids))
        if self.trajectory_filter_active and self.trajectory_filter is not None:
            query += SQLQueries.AND.value.format(filter=self.trajectory_filter)

        data = self._get_data_from_query(query)
        if data is None:
            return None
        return DataRecord(_data=data, _column_names=(Column.TRAJECTORY_ID.value,), _name=Column.TRAJECTORY_ID.value)

    def _get_data_from_query(self, query: str) -> Optional[DataFrame]:
        """
        Gets the data from the database using the given query. Checks if the connection is valid.
        Also checks if the data is in the correct format.
        :param query: The query as a string.
        :param connection: The connection to the database as a DatabaseConnection object.
        :return: The data as a DataFrame or None if an error occurred.
        """
        connection: Optional[Connection] = self.get_connection()
        if connection is None:
            self.throw_error(ErrorMessage.DATASET_DATA_ERROR)
            return None

        data: Optional[DataFrame] = self.query_sql(sql_query=query, connection=connection)
        self.database_connection.post_connection()

        if data is None:
            self.throw_error(ErrorMessage.DATASET_DATA_ERROR, "while querying the database with: " + query)
            return None

        return data

    def _get_dataset_uuids(self) -> List[UUID]:
        return self.dataset_facade.get_active_datasets()
