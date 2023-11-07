from typing import Optional

import pandas
from pandas import DataFrame
from sqlalchemy import Connection, text
from sqlalchemy.exc import SQLAlchemyError

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.database.database_connection import DatabaseConnection
from src.model.error_handler import ErrorHandler

UUID_COLUMN_NAME: str = "dataset_id"


class DatabaseComponent(ErrorHandler):
    """
    Represents an abstract component of the database that allows querying.
    """

    def __init__(self, database_connection: Optional[DatabaseConnection]):
        """
        Sets the connection to the database.
        :param database_connection: the connection to the database as a DatabaseConnection object
        """
        super().__init__()
        self.database_connection: Optional[DatabaseConnection] = database_connection

    def query_sql(self, sql_query: str, connection: Connection, read: bool = True) -> Optional[DataFrame]:
        """
        queries the database with the given sql query. If pandas_query is true, the query will be executed with pandas,
        otherwise with sqlalchemy. If executed with pandas, the result will be a pandas dataframe, otherwise nothing
        is returned.
        :param sql_query: the sql query
        :param connection: the connection
        :param pandas_query: if true, the query will be executed with pandas, otherwise with sqlalchemy
        :return: the result of the query
        """
        if read:
            return self.read_from_sql(sql_query, connection)

        return DataFrame() if self.write_to_sql(sql_query, connection) else None

    def read_from_sql(self, sql_query: str, connection: Connection) -> Optional[DataFrame]:
        """
        queries the database with the given sql query with pandas and returns the result as a dataframe.
        :param sql_query: the sql query
        :param connection: the connection as a sqlalchemy connection
        :return: the result of the query
        """
        try:
            return pandas.read_sql_query(text(sql_query), connection)
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_QUERY_ERROR, str(err))
            return None

    def write_to_sql(self, sql_query: str, connection: Connection) -> bool:
        """
        Queries the database with the given sql query with sqlalchemy.
        :param sql_query: the sql query
        :param connection: the connection as a sqlalchemy connection
        """
        try:
            connection.execute(text(sql_query))
            return True
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_QUERY_ERROR, str(err))
            return False

    def get_connection(self) -> Optional[Connection]:
        """
        Gets the connection to the database.
        :return: The connection to the database.
        """
        try:
            connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_ERROR, str(e))
            return None

        return connection
