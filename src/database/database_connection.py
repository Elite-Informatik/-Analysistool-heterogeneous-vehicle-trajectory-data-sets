from sqlalchemy import create_engine

from src.database.query_logging import log_query


class DatabaseConnection:

    def __init__(self, host: str, user: str, password: str, database: str, port: str):
        """
        Sets the connection parameters for the database.
        :param host: the host of the database
        :param user: the user of the database
        :param password: the password of the database
        :param database: the database name
        :param port: the port of the database
        """
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.database: str = database
        self.port: str = port
        # create engine with the given parameters.
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}', echo=False,
                                    pool_size=20, max_overflow=30)
        self.connection = self.engine.connect()

    def get_connection(self):
        """
        Returns the connection to the database. If the connection is closed or not set, a new connection is created.
        :return: The connection to the database.
        """
        self.connection = self.engine.connect()
        if self.connection is None or self.connection.closed:
            self.connection = self.engine.connect()
            log_query("Connection established.")
        else:
            log_query("Connection already established.")
        return self.connection

    def post_connection(self):
        """
        Closes the connection to the database.
        """
        """if self.connection is not None and not self.connection.closed:
            self.connection.commit()
            log_query("Connection still open.")
        else:
            log_query("Connection closed.")"""
        self.connection.commit()
        self.connection.close()
        log_query("Connection closed.")

    def recover(self):
        """
        Recovers the connection to the database.
        """
        self.connection.rollback()
        self.connection.commit()
        self.connection.close()

    def __del__(self):
        """
        Closes the connection to the database.
        """
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
