from re import compile
from re import match
from typing import Optional
from uuid import UUID

import pandas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from src.data_transfer.content.column import Column
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.record.data_record import DataRecord
from src.data_transfer.record.data_set_record import DatasetRecord
from src.database.query_logging import log_query
from src.database.sql_querys import SQLQueries
from src.model.error_handler import ErrorHandler

GEOMETRY: str = "geometry"
REGEX = compile('.*')
SQL_SUFFIX = ";"

APPEND: dict = {True: "append", False: "replace"}


class TableAdapter(ErrorHandler):
    """
    represents an adapter for a table containing a dataset
    """

    def __init__(self, database_connection):
        super().__init__()
        self.database_connection = database_connection
        self.key = None
        self.size = None
        self.uuid = None
        self.db_key = None

    def from_existing_table(self, name: str, key: str, uuid: UUID, size: int = 0):
        """
        creates a table adapter from an existing table
        """
        self.name = name
        self.key = key
        self.uuid = uuid
        self.size = size

    def insert_data(self, data: pandas.DataFrame, append=False, add_geometry: bool = True) -> bool:
        """
        inserts the given data into the table
        :param append: if true, the data will be appended to the table, otherwise the table will be replaced
        :param data: the data
        """
        if match(REGEX, self.key) is None:
            self.throw_error(ErrorMessage.DATASET_NAME_INVALID, msg=f"Dataset name '{self.key}' is not valid!")
            return False

        """# Aggregate longitude and latitude
        stack_lonlat = data_record.data.agg({'longitude': np.stack, 'latitude': np.stack})
        # Create the LineString using aggregate values
        line_str_objects = list()
        for o in list(zip(*stack_lonlat)):
            line_str_objects.append("LineString(" + str(o[0]) + " " + str(o[1]) + ")")

        data_record.data["geometry"] = line_str_objects
        """

        if add_geometry:
            data[GEOMETRY] = data.apply(lambda row:
                                        "LineString(" + str(row['longitude']) +
                                        " " +
                                        str(row['latitude']) + ")", axis=1)

        try:
            connection = self.database_connection.get_connection()
            log_query("Creating table " + self.key)
            data.to_sql(name=self.key, con=connection, if_exists=APPEND[append], index=False)
            self.database_connection.post_connection()
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(err))
            self.database_connection.recover()
            return False

        connection = self.database_connection.get_connection()
        # Get size
        try:
            query = SQLQueries.TABLE_SIZE.value.format(tablename=self.key) + SQL_SUFFIX
            log_query(query)
            query = text(query)
            size_cursor = connection.execute(query)
            self.size = size_cursor.fetchone()[0]
            size_cursor.close()
            self.database_connection.post_connection()
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(err))
            self.database_connection.recover()
            return False

        return True

    def delete_table(self) -> bool:
        """
        deletes this table
        """
        connection = self.database_connection.get_connection()
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
        connection = self.database_connection.get_connection()
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
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_IMPOSSIBLE, str(err))
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
