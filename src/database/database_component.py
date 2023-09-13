from typing import Optional

import pandas
from pandas import DataFrame
from sqlalchemy import Connection
from sqlalchemy.exc import SQLAlchemyError

from src.data_transfer.content.error import ErrorMessage
from src.model.error_handler import ErrorHandler


class DatabaseComponent(ErrorHandler):
    """
    Represents an abstract component of the database that allows querying.
    """

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

        return self.write_to_sql(sql_query, connection)

    def read_from_sql(self, sql_query: str, connection: Connection) -> DataFrame:
        """
        queries the database with the given sql query with pandas and returns the result as a dataframe.
        :param sql_query: the sql query
        :param connection: the connection as a sqlalchemy connection
        :return: the result of the query
        """
        try:
            return pandas.read_sql_query(sql_query, connection)
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_QUERY_ERROR, str(err))
            return DataFrame()

    def write_to_sql(self, sql_query, connection) -> None:
        """
        Queries the database with the given sql query with sqlalchemy.
        :param sql_query: the sql query
        :param connection: the connection as a sqlalchemy connection
        """
        try:
            connection.execute(sql_query)
        except SQLAlchemyError as err:
            self.throw_error(ErrorMessage.DATABASE_QUERY_ERROR, str(err))