from re import compile
from re import match
from typing import Optional
from uuid import UUID

import pandas
import pandas as pd
from pandas import DataFrame
from sqlalchemy import Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from src.data_transfer.content.column import Column
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.data_transfer.record.data_record import DataRecord
from src.data_transfer.record.data_set_record import DatasetRecord
from src.database.database_connection import DatabaseConnection
from src.database.query_logging import log_query
from src.database.sql_querys import SQLQueries
from src.model.error_handler import ErrorHandler

GEOMETRY: str = "geometry"
REGEX = compile('.*')
SQL_SUFFIX = ";"

APPEND: dict = {True: "append", False: "replace"}

META_TABLE_COLUMNS: list = ["name", "uuid", "size"]


class TableAdapter(ErrorHandler):
    """
    represents an adapter for a table containing a dataset
    """

    def __init__(self, database_connection):
        super().__init__()
        self.database_connection: DatabaseConnection = database_connection
        self.key = None
        self.size = None
        self.uuid = None
        self.db_key = None
        self.name = None

    def from_existing_table(self, name: str, uuid: UUID, size: int = 0):
        """
        creates a table adapter from an existing table
        """
        self.name = name
        self.uuid = uuid
        self.size = size

    def insert_data(self, data: pandas.DataFrame, add_geometry: bool = True) -> bool:
        """
        inserts the given data into the table
        :param append: if true, the data will be appended to the table, otherwise the table will be replaced
        :param data: the data
        """

        if add_geometry:
            data[GEOMETRY] = data.apply(lambda row:
                                        "LineString(" + str(row['longitude']) +
                                        " " +
                                        str(row['latitude']) + ")", axis=1)
        dataset_table_name: str = self.database_connection.data_table
        metadata_table_name: str = self.database_connection.meta_table
        try:
            connection: Connection = self.database_connection.get_connection()
            if not isinstance(connection, Connection):
                raise DatabaseConnectionError("SQLAlchemy returned non connection object!")
            data["Dataset_ID"] = self.uuid
            data.to_sql(name=dataset_table_name, con=connection.engine, if_exists=APPEND[True], index=False)
            DataFrame(data={META_TABLE_COLUMNS[0]: [self.name], META_TABLE_COLUMNS[1]: [self.uuid],
                            META_TABLE_COLUMNS[2]: [self.size]}).to_sql(
                name=metadata_table_name,
                con=connection.engine,
                if_exists=APPEND[True],
                index=False)
            self.database_connection.post_connection()

        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(e))
            return False

        """      except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(err))
            self.database_connection.recover()
            return False"""

        #self.size = 0  # size_cursor.fetchone()[0] todo: add size calculation


        return True

    def delete_table(self) -> bool:
        """
        deletes this table
        """
        try:
            connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(e))
            return False
        query = SQLQueries.DROPTABLE.value.format(tablename=self.key)
        log_query(query)
        query = text(query)
        try:
            delete_cursor = connection.execute(query)
            delete_cursor.close()
            self.database_connection.post_connection()
        except SQLAlchemyError as e:
            self.throw_error(ErrorMessage.DATASET_NOT_EXISTING, str(e))
            self.database_connection.recover()
            return False
        return True

    def to_data_set_record(self) -> DatasetRecord:
        """
        gets the metadata of the dataset in this table
        :return the dataset record
        """
        return DatasetRecord(self.name, self.size)

    def query_sql(self, query: str, pandas_query: bool = True) -> Optional[DataRecord]:
        """
        gets the by the query filtered data
        :param query:   the sql query
        :return the data
        """
        try:
            connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(e))
            return None
        query = query.format(tablename=self.key) + SQL_SUFFIX
        log_query(query)
        query = text(query)
        try:
            if pandas_query:
                result = pandas.read_sql_query(query, connection)
            else:
                connection.execute(query)
                result = None
            self.database_connection.post_connection()
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_QUERY_ERROR, str(err))
            self.database_connection.recover()
            return None

        """try:
            with self.engine.connect() as connection:
                try:
                    results = connection.execute(text(query))
                except SQLAlchemyError as err:
                    self.throw_error(ErrorMessage.DATASET_NOT_EXISTING, str(err))
                    return None

        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(err))
            return None"""

        return DataRecord(self.key, tuple([column.value for column in Column]), result)

    def get_uuid(self) -> UUID:
        """
        the uuid of the table
        """
        return self.uuid
