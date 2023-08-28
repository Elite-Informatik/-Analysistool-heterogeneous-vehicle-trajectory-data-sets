import random
import re as re
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID
from uuid import uuid4

import pandas as pd
from sqlalchemy import Connection
from sqlalchemy.sql import text

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.exception.custom_exception import DatabaseConnectionError
from src.data_transfer.record import DataRecord
from src.data_transfer.record import DatasetRecord
from src.database.database_connection import DatabaseConnection
from src.database.dataset_facade import DatasetFacade
from src.database.postgre_sql_data_facade import PostgreSQLDataFacade
from src.database.query_logging import log_query
from src.database.sql_querys import SQLQueries
from src.database.table_adapter import TableAdapter

RANDOM_MAX: int = 1000000000
DATABASE: str = "database"
USER: str = "user"
PASSWORD: str = "password"
HOST: str = "host"
PORT: str = "port"
DATA_TABLE: str = "data_table"
META_TABLE: str = "meta_table"
META_TABLE_COLUMNS: list = ["name", "uuid", "size"]
PANDAS_TABLE: pd.DataFrame = pd.DataFrame({"table_name": [], "table_uuid": [], "table_size": []})
INVALID_PREFIX: str = "Other Dataset: "


class PostgreSQLDatasetFacade(DatasetFacade):
    """
    Postgre Adapter for the database
    """

    def __init__(self, postgre_sql_data_facade: PostgreSQLDataFacade):
        super().__init__()
        self.postgre_sql_data_adapter = postgre_sql_data_facade
        self.tables_table: TableAdapter = None
        self.tables_table_name: str = ""
        self.table_adapters = {}
        self.table_adapter: Optional[TableAdapter] = None
        self.database_connection: Optional[DatabaseConnection] = None

    def set_connection(self, connection: Dict[str, str]) -> bool:
        if not (DATABASE in connection.keys() and USER in connection.keys() and PASSWORD in connection.keys() and
                HOST in connection.keys() and PORT in connection.keys()):
            self.throw_error(ErrorMessage.INVALID_TYPE, "The connection is invalid.")
            return False
        self.tables_table_name = connection[META_TABLE]
        self.database_connection = DatabaseConnection(
            database=connection[DATABASE],
            user=connection[USER],
            password=connection[PASSWORD],
            host=connection[HOST],
            port=connection[PORT],
            meta_table=connection[META_TABLE],
            data_table=connection[DATA_TABLE],
        )
        return True

    def get_uuids(self) -> List[UUID]:
        connection = self.database_connection.get_connection()
        uuids = pd.read_sql_table(table_name=self.tables_table_name, con=connection, columns=["uuid"]).drop_duplicates()
        uuids = [UUID(dataset_id) for dataset_id in uuids["uuid"].tolist()]
        return uuids

    def get_data_set_meta(self, dataset_uuid: UUID) -> Optional[DatasetRecord]:
        if not (dataset_uuid in self.get_uuids()):
            raise InvalidUUID("The UUID ({}) does not appear to exist.".format(dataset_uuid))

        connection = self.database_connection.get_connection()
        dataset_record = pd.read_sql_table(table_name=self.tables_table_name, con=connection,
                                           columns=META_TABLE_COLUMNS).drop_duplicates()
        dataset_record = dataset_record[dataset_record["uuid"] == str(dataset_uuid)]
        dataset_record = DatasetRecord(dataset_record["name"].tolist()[0],
                                       dataset_record["size"].tolist()[0])
        return dataset_record

    def delete_dataset(self, dataset_uuid: UUID) -> bool:
        if not (dataset_uuid in self.table_adapters.keys()):
            self.throw_error(ErrorMessage.DATASET_NOT_EXISTING,
                             "The UUID ({}) does not appear to exist.".format(dataset_uuid))
            return False

        table_adapter = self.table_adapters[dataset_uuid]
        if not table_adapter.delete_table():
            for error in table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return False
        delete_query = SQLQueries.DELETE.value.format(tablename=self.tables_table_name,
                                                      key_column="table_uuid = " + "'" +
                                                                 self.table_adapters[dataset_uuid].key + "'")
        self.tables_table.query_sql(delete_query, False)
        del self.table_adapters[dataset_uuid]
        return True

    def set_current_dataset(self, dataset_uuid: UUID) -> bool:
        if not (dataset_uuid in self.table_adapters.keys()):
            self.throw_error(ErrorMessage.DATASET_NOT_EXISTING,
                             "The UUID ({}) does not appear to exist.".format(dataset_uuid))
            return False

        table_adapter = self.table_adapters.get(dataset_uuid)
        self.postgre_sql_data_adapter.set_table_adapter(table_adapter)
        return True

    def add_dataset(self, data: DataRecord, append: bool = False) -> Optional[UUID]:
        # number_of_tables = len(self.table_adapters)
        random_int = random.randint(0, RANDOM_MAX)
        uuid = uuid4()
        name = data.name
        # key = "trajectory_analysis_tool_" + str(random_int) + "_" + re.sub(r'[^a-zA-Z]', '', name)

        df: pd.DataFrame = data.data

        data_table_name = self.database_connection.data_table
        # df.to_sql(name=data_table_name, con=self.database_connection.engine, if_exists="append", index=False)

        try:
            connection: Connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_ERROR, e.args)
            return None

        for data_set_name, size in self.get_tables_from_sql():
            if data_set_name == name:
                uuid = connection.execute(text(SQLQueries.SELECT_UUID_FROM_TABLE.value.format(
                    meta_table_name=self.database_connection.meta_table,
                    tablename=data_set_name
                ))).fetchone()[0]
                break

        table_adapter = TableAdapter(self.database_connection)
        table_adapter.from_existing_table(name=name, uuid=uuid, size=df.memory_usage(index=True).sum())

        table_adapter.insert_data(data=df, add_geometry=False)

        self.database_connection.post_connection()

        return table_adapter.uuid

    def get_data_sets_as_dict(self) -> Dict[str, int]:
        if self.table_adapter is None:
            self.table_adapter = TableAdapter(self.database_connection)

        datasets: Optional[pd.DataFrame] = self.table_adapter.query_sql(SQLQueries.SELECT_FROM.value.format(
            columns=("name, size"),
            tablename=self.tables_table_name), False
        )
        if datasets is None:
            return None
        return datasets.to_dict()

    def set_data_sets_as_dict(self) -> Optional[List[UUID]]:

        return self.get_uuids()

    def get_tables_from_sql(self) -> Optional[List[Tuple[str, int]]]:
        try:
            database_connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_ERROR, ErrorMessage.DETAIL_MESSAGE.value + str(e.args))
            return None
        query = SQLQueries.GET_ALL_TABLES.value
        log_query(query)
        cursor = database_connection.execute(text(query))
        tables = cursor.fetchall()
        if (self.tables_table_name,) not in tables:
            self.create_tables_table()
        query = SQLQueries.GET_TABLES_FROM_TABLE_WITH_SIZE.value.format(tablename=self.tables_table_name)
        log_query(query)
        cursor = database_connection.execute(text(query))

        rows = cursor.fetchall()
        cursor.close()
        tables = []
        # for name, size in rows:
        for name, size in rows:
            tables.append((name, size))
        return tables

    def get_columns(self, table_name: str) -> List[str]:
        database_connection = self.database_connection.get_connection()
        cursor = database_connection.execute(text(SQLQueries.GET_COLUMNS.value.format(tablename=table_name)))
        columns = cursor.fetchall()
        cursor.close()
        return columns

    def create_tables_table(self):

        try:
            connection: Connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_ERROR, ErrorMessage.DETAIL_MESSAGE.value + str(e.args))
            return
        meta_table: str = self.database_connection.meta_table
        connection.execute(text(SQLQueries.CREATETABLE.value.format(tablename=text(meta_table),
                                                                    columns=META_TABLE_COLUMNS[0] + " TEXT, "
                                                                            + META_TABLE_COLUMNS[1] + " TEXT, "
                                                                            + META_TABLE_COLUMNS[2] + " DOUBLE "
                                                                                                      "PRECISION")))
        self.database_connection.post_connection()
        # pd.DataFrame({"name": [], "uuid": [], "size": []}).to_sql(name=meta_table,
        #                                                          con=connection.engine,
        #                                                          if_exists="append",
        #                                                          index=False)

    def table_exists(self, table_name: str, all_database: bool = False) -> bool:

        tables = self.get_tables_from_sql()

        if all_database:
            return table_name in tables
        for key, value in self.table_adapters.items():
            if value.name == table_name:
                return True
        return False
