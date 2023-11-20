from typing import Optional, List, Set

from pandas import DataFrame, Series
from sqlalchemy import text, TextClause, Connection
from uuid import UUID

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.data_transfer.record import DatasetRecord
from src.database.database_connection import DatabaseConnection
from src.database.database_component import DatabaseComponent, UUID_COLUMN_NAME
from src.database.sql_querys import SQLQueries

META_TABLE_COLUMNS: list = ["name", "dataset_id", "size"]
META_TABLE_NAME = 0
META_TABLE_UUID = 1
META_TABLE_SIZE = 2


class DatasetMetaTable(DatabaseComponent):
    """
    A class representing the table consisting of the meta information of the datasets.
    """
    _table_exists: bool = False

    def __init__(self, connection: DatabaseConnection):
        super().__init__(database_connection=connection)
        self.name = connection.meta_table
        if not DatasetMetaTable._table_exists and not self._exists(self.name):
            table_created: bool = self._create_table()
            DatasetMetaTable._table_exists = table_created
        else:
            DatasetMetaTable._table_exists = True
        self.check_meta_table_is_valid()

    def _exists(self, table_name: str) -> bool:
        """
        Checks if the meta_table already exists in the database.
        :return: True if the Table exists and False if it doesn't or an error occurred.
        """
        connection: Connection = self.get_connection()
        if connection is None:
            return False

        query: str = SQLQueries.GET_ALL_TABLES.value

        tables: DataFrame = self.query_sql(sql_query=query, connection=connection, read=True)

        if tables is None:
            raise DatabaseConnectionError(ErrorMessage.DATABASE_QUERY_ERROR.value + query + "\n while checking if "
                                                                                            "the meta_table table "
                                                                                            "exists in the database."
                                                                                            " with errors: " + str(
                [error.args for error in self.get_errors()]))

        return tables.isin([table_name]).any().any()

    def _create_table(self) -> bool:
        """
        Creates the meta_table in the database.
        :return: True if the table was created successfully and False if an error occurred.
        """
        connection: Connection = self.get_connection()
        if connection is None:
            return False

        query: str = SQLQueries.CREATE_TABLE.value.format(table_name=text(self.name),
                                                          columns=META_TABLE_COLUMNS[META_TABLE_NAME] + " TEXT, "
                                                                  + META_TABLE_COLUMNS[META_TABLE_UUID] + " TEXT, "
                                                                  + META_TABLE_COLUMNS[META_TABLE_SIZE] + " DOUBLE "
                                                                                                          "PRECISION")

        self.query_sql(sql_query=query, connection=connection, read=False)
        self.database_connection.post_connection()

        return True

    def add_table(self, dataset_name: str, dataset_uuid: UUID, dataset_size: int) -> bool:
        """
        Adds a table to the meta_table.
        :param dataset_name: The name of the dataset.
        :param dataset_uuid: The uuid of the dataset.
        :param dataset_size: The size of the dataset. -1 is the default value for an illegal size.
        """
        if dataset_size == -1:
            raise ValueError(ErrorMessage.DATASET_ILLEGAL_DATASET_ADD.value)
        if self.contains(dataset_uuid=dataset_uuid):
            raise ValueError(ErrorMessage.DATASET_UUID_COLLISION.value)
        connection: Connection = self._assert_table_exists_get_connection()
        if connection is None:
            self.throw_error(ErrorMessage.DATASET_ADD_META_ERROR, "uuid: " + str(dataset_uuid))
            return False

        dataset_meta_data: DataFrame = DataFrame(data={META_TABLE_COLUMNS[META_TABLE_NAME]: [dataset_name],
                                                       META_TABLE_COLUMNS[META_TABLE_UUID]: [dataset_uuid],
                                                       META_TABLE_COLUMNS[META_TABLE_SIZE]: [dataset_size]})
        try:
            dataset_meta_data.to_sql(name=self.name, con=connection.engine, if_exists="append", index=False)
        except ValueError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_ERROR, "uuid: " + str(dataset_uuid))
            self.throw_error(ErrorMessage.DATASET_ADD_META_ERROR, "uuid: " + str(dataset_uuid))
            return False
        self.database_connection.post_connection()

    def adjust_size(self, dataset_uuid: UUID, new_size: int) -> bool:
        """
        Adjusts the size of a dataset in the meta_table.
        :param dataset_uuid: The uuid of the dataset.
        :param new_size: The new size of the dataset.
        """
        connection: Connection = self._assert_table_exists_get_connection()
        if connection is None:
            self.throw_error(ErrorMessage.DATASET_SIZE_NOT_UPDATED, "uuid: " + str(dataset_uuid))
            return False

        query: str = SQLQueries.UPDATE_DATASET_SIZE.value.format(meta_table_name=self.name,
                                                                 column=META_TABLE_COLUMNS[META_TABLE_SIZE],
                                                                 dataset_uuid=dataset_uuid,
                                                                 new_size=new_size,
                                                                 uuid_column=META_TABLE_COLUMNS[META_TABLE_UUID])

        query_success_dataframe: Optional[DataFrame] = self.query_sql(sql_query=query, connection=connection,
                                                                      read=False)
        self.database_connection.post_connection()

        if query_success_dataframe is None:
            self.throw_error(ErrorMessage.DATASET_SIZE_NOT_UPDATED, "uuid: " + str(dataset_uuid))
            return False

        return True

    def increase_size(self, dataset_uuid: UUID, size_increase: int) -> bool:
        """
        Increases the size of a dataset in the meta_table by the given size_increase.
        :param dataset_uuid: The uuid of the dataset.
        :param size_increase: The size increase of the dataset.
        :return: True if the size was increased successfully and False if an error occurred.
        """
        size: Optional[int] = self.get_size(dataset_uuid=dataset_uuid)
        if size is None:
            self.throw_error(ErrorMessage.DATASET_SIZE_NOT_UPDATED, "uuid: " + str(dataset_uuid))
            return False
        return self.adjust_size(dataset_uuid=dataset_uuid, new_size=size + size_increase)

    def get_size(self, dataset_uuid: UUID) -> Optional[int]:
        """
        Gets the size of a dataset in the meta_table.
        :param dataset_uuid: The uuid of the dataset of the size to be determined.
        """
        meta_data: Optional[DataFrame] = self.get_meta_data(dataset_uuid=dataset_uuid)
        if meta_data is None:
            return None
        size: int = meta_data[META_TABLE_COLUMNS[META_TABLE_SIZE]].iloc[0]
        return size

    def contains(self, dataset_uuid: UUID) -> bool:
        """
        Checks if the meta_table contains the dataset.
        :param dataset_uuid: The uuid of the dataset to check.
        """

        dataset_meta_data: Optional[DataFrame] = self._get_meta_data_df(dataset_uuid=dataset_uuid)
        if dataset_meta_data is None:
            return False
        return not dataset_meta_data.empty

    def get_meta_data(self, dataset_uuid: UUID) -> Optional[DataFrame]:
        """
        Gets the metadata of a dataset as a Dataframe. Returns None if the connection to the database failed or if no
        dataset with the given uuid exists.

        :param dataset_uuid: The dataset to get the metadata of.
        :return: The metadata of the dataset as an optional Dataframe.
        :raises RuntimeError: If the database contains multiple datasets with the same uuid or if the column names of
        the returned Dataframe (from the database) are not the same as the expected ones.
        This would indicate a change in the database or an error in the code.
        """

        dataset_meta_data: Optional[DataFrame] = self._get_meta_data_df(dataset_uuid=dataset_uuid)

        if dataset_meta_data is None or dataset_meta_data.empty:
            self.throw_error(ErrorMessage.DATASET_NOT_EXISTING, "uuid: " + str(dataset_uuid))
            return None

        if dataset_meta_data.shape[0] > 1:
            raise RuntimeError(ErrorMessage.DATABASE_MULTIPLE_DATASETS_WITH_SAME_UUID.value + " for uuid: " + str(
                dataset_uuid))
        dataset_columns: List[str] = list(dataset_meta_data.columns)

        if len(dataset_columns) != len(META_TABLE_COLUMNS) \
                or dataset_columns[0] != META_TABLE_COLUMNS[0] or dataset_columns[1] != META_TABLE_COLUMNS[1] \
                or dataset_columns[2] != META_TABLE_COLUMNS[2]:
            raise RuntimeError(ErrorMessage.DATABASE_WRONG_COLUMN_NAMES.value + "expected: " + str(
                META_TABLE_COLUMNS) + " got: " + str(dataset_columns))

        self.database_connection.post_connection()

        return dataset_meta_data

    def _get_meta_data_df(self, dataset_uuid: UUID) -> Optional[DataFrame]:
        """
        Helper method to get the metadata as a dataframe of a given dataset specified by its uuid.
        :returns None if an error occurs, an empty dataframe if the dataset does not exist and a dataframe with the
        metadata of the dataset if it exists. The name of the columns of the dataframe are the same as the ones in the
        request below.
        """
        connection: Connection = self.get_connection()
        if connection is None:
            return None
        query: str = SQLQueries.SELECT_DATASET_METADATA.value.format(columns=f"{META_TABLE_COLUMNS[META_TABLE_NAME]}, "
                                                                             f"{META_TABLE_COLUMNS[META_TABLE_UUID]}, "
                                                                             f"{META_TABLE_COLUMNS[META_TABLE_SIZE]}",
                                                                     uuid=dataset_uuid,
                                                                     uuid_column=META_TABLE_COLUMNS[META_TABLE_UUID],
                                                                     meta_table_name=self.name)

        return self.query_sql(sql_query=query, connection=connection)


    def get_meta_data_as_record(self, dataset_uuid: UUID) -> Optional[DatasetRecord]:
        """
        Gets the metadata of a dataset as a DatasetRecord. Returns None if the connection to the database failed or if
        no dataset with the given uuid exists.
        """
        dataframe: Optional[DataFrame] = self.get_meta_data(dataset_uuid)
        if dataframe is None:
            return None
        name: str = dataframe[META_TABLE_COLUMNS[META_TABLE_NAME]].iloc[0]
        size: int = dataframe[META_TABLE_COLUMNS[META_TABLE_SIZE]].iloc[0]
        return DatasetRecord(_name=name, _size=size)

    def remove_dataset(self, dataset_uuid: UUID) -> bool:
        """
        Removes a dataset from the meta_table.
        """
        connection: Connection = self._assert_table_exists_get_connection()
        if connection is None:
            self.throw_error(ErrorMessage.DATASET_NOT_DELETED)
            return False

        query: str = SQLQueries.DELETE_DATASET.value.format(uuid=dataset_uuid,
                                                            table_name=self.name,
                                                            column=META_TABLE_COLUMNS[META_TABLE_UUID])

        self.query_sql(sql_query=query, connection=connection, read=False)

        self.database_connection.post_connection()

        return True

    def get_all_datasets(self) -> List[UUID]:
        """
        Gets the uuids of every dataset referenced the meta table.
        :returns: A list of UUIDs corresponding to the datasets in the meta table.
        """
        connection: Connection = self._assert_table_exists_get_connection()
        if connection is None:
            self.throw_error(ErrorMessage.ALL_DATASETS_LOAD_ERROR)
            return []
        query: str = SQLQueries.GET_COLUMN_FROM_TABLE.value.format(column=META_TABLE_COLUMNS[META_TABLE_UUID],
                                                                   table_name=self.name)

        uuid_dataframe: DataFrame = self.query_sql(sql_query=query, connection=connection)

        if uuid_dataframe is None:
            self.throw_error(ErrorMessage.ALL_DATASETS_LOAD_ERROR)
            return []

        columns: List[str] = list(uuid_dataframe.columns)
        # raises a RuntimeError as this should not be possible
        if len(columns) != 1 or META_TABLE_COLUMNS[1] not in columns:
            raise RuntimeError(f"The data loaded from the Database is not in the correct format. Expected: "
                               f"[{META_TABLE_COLUMNS[1]}], but got: {columns}")

        uuids = uuid_dataframe[META_TABLE_COLUMNS[1]].to_list()
        return [UUID(uuid) for uuid in uuids]

    def _assert_table_exists_get_connection(self) -> Optional[Connection]:
        """
        Checks if the meta table exists and returns the connection to the database.
        """
        if not self._table_exists:
            self.throw_error(ErrorMessage.META_TABLE_NOT_EXISTING, "There might be a problem with the database.")
            return None

        connection: Connection = self.get_connection()
        if connection is None:
            return None

        return connection

    def check_meta_table_is_valid(self):
        """
        A private method to check if the meta table is synced with the main table.
        It checks if the meta table and the main table contain the same ids.
        """
        meta_ids: List[UUID] = self.get_all_datasets()
        data_table_name: str = self.database_connection.data_table
        query: str = SQLQueries.GET_DISTINCT_VALUES.value.format(column=UUID_COLUMN_NAME,
                                                                 table_name=data_table_name)
        connection: Connection = self._assert_table_exists_get_connection()

        # first startup of the program
        if len(meta_ids) == 0 and not self._exists(data_table_name):
            return

        id_df: DataFrame = self.query_sql(sql_query=query, connection=connection)
        if id_df is None:
            raise RuntimeError("Could not check if the meta table is synced with the main table.")

        table_ids: List[UUID] = [UUID(uuid_str) for uuid_str in id_df[UUID_COLUMN_NAME].to_list()]

        # both tables should have the same amount of ids.
        if len(meta_ids) != len(table_ids):
            self.throw_error(ErrorMessage.META_TABLE_NOT_SYNCED,
                             "meta_ids: " + str(meta_ids) + " table_ids: " + str(table_ids))
            return

        # the meta table should not contain any duplicate ids.
        id_set: Set[UUID] = set(meta_ids)
        if len(id_set) != len(meta_ids):
            self.throw_error(ErrorMessage.META_TABLE_DUPLICATE_UUIDS)
            return

        # the meta table and the main table should contain the same ids.
        if id_set != set(table_ids):
            self.throw_error(ErrorMessage.META_TABLE_NOT_SYNCED,
                             "meta_ids: " + str(meta_ids) + " table_ids: " + str(table_ids))
            return

