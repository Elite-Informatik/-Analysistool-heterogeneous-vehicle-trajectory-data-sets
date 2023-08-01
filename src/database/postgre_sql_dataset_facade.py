import random
import re as re
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID
from uuid import uuid4

import pandas as pd
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
TABLES_TABLE: str = "initial_table"
PANDAS_TABLE: pd.DataFrame = pd.DataFrame({"table_name": [], "table_uuid": [], "table_size": []})
INVALID_PREFIX: str = "Other Dataset: "


class PostgreSQLDatasetFacade(DatasetFacade):
    """
    Postgre Adapter for the database
    """

    def __init__(self, postgre_sql_data_facade: PostgreSQLDataFacade):
        super().__init__()
        self.postgre_sql_data_adapter = postgre_sql_data_facade
        self.tables_table = None
        self.table_adapters = {}
        self.database_connection: Optional[DatabaseConnection] = None

    def set_connection(self, connection: Dict[str, str]) -> bool:
        if not (DATABASE in connection.keys() and USER in connection.keys() and PASSWORD in connection.keys() and
                HOST in connection.keys() and PORT in connection.keys()):
            self.throw_error(ErrorMessage.INVALID_TYPE, "The connection is invalid.")
            return False

        self.database_connection = DatabaseConnection(
            database=connection[DATABASE],
            user=connection[USER],
            password=connection[PASSWORD],
            host=connection[HOST],
            port=connection[PORT])
        return True

    def get_data_set_meta(self, dataset_uuid: UUID) -> Optional[DatasetRecord]:
        if not (dataset_uuid in self.table_adapters.keys()):
            raise InvalidUUID("This UUID is not existing.")

        data = self.table_adapters.get(dataset_uuid).to_data_set_record()
        if data is None:
            for table in self.table_adapters:
                for error in table.get_errors():
                    self.throw_error(error.error_type, error.args)
            return None
        return data

    def delete_dataset(self, dataset_uuid: UUID) -> bool:
        if not (dataset_uuid in self.table_adapters.keys()):
            self.throw_error(ErrorMessage.DATASET_NOT_EXISTING, "This UUID is not existing.")
            return False

        table_adapter = self.table_adapters[dataset_uuid]
        if not table_adapter.delete_table():
            for error in table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return False
        delete_query = SQLQueries.DELETE.value.format(tablename=TABLES_TABLE,
                                                      key_column="table_uuid = " + "'" +
                                                                 self.table_adapters[dataset_uuid].key + "'")
        self.tables_table.query_sql(delete_query, False)
        del self.table_adapters[dataset_uuid]
        return True

    def set_current_dataset(self, dataset_uuid: UUID) -> bool:
        if not (dataset_uuid in self.table_adapters.keys()):
            self.throw_error(ErrorMessage.DATASET_NOT_EXISTING, "This UUID is not existing.")
            return False

        table_adapter = self.table_adapters.get(dataset_uuid)
        self.postgre_sql_data_adapter.set_table_adapter(table_adapter)
        return True

    def add_dataset(self, data: DataRecord, append: bool = False) -> Optional[UUID]:
        number_of_tables = len(self.table_adapters)
        random_int = random.randint(0, RANDOM_MAX)
        uuid = uuid4()
        name = data.name
        key = "trajectory_analysis_tool_" + str(random_int) + "_" + re.sub(r'[^a-zA-Z]', '', name)

        table_adapter = TableAdapter(self.database_connection)
        table_adapter.from_existing_table(name=name, uuid=uuid, key=key)

        already_existing = False
        for uuid_key, value in self.table_adapters.items():
            if value.name == data.name:
                already_existing = True
                uuid = uuid_key
                table_adapter = self.table_adapters[uuid]

        if not already_existing:
            append = False

        if not table_adapter.insert_data(data.data, append=append, add_geometry=True):
            for error in table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return None

        if not already_existing:
            self.table_adapters[table_adapter.uuid] = table_adapter
            insert = pd.DataFrame({"table_name": [table_adapter.name],
                                   "table_uuid": [table_adapter.key],
                                   "table_size": [table_adapter.size]})
            self.tables_table.insert_data(insert, append=True, add_geometry=False)
        if already_existing:
            update_query = SQLQueries.UPDATE.value.format(tablename="initial_table",
                                                          update_columns=("table_size = '" + str(table_adapter.size)
                                                                          + "'"),
                                                          key_column="table_uuid = '" + key + "'")
            self.tables_table.query_sql(update_query, False)

        return table_adapter.uuid

    def get_data_sets_as_dict(self) -> Dict[str, int]:
        data_sets: dict[str, int] = {}
        for key, table_adapter in self.table_adapters.items():
            table_adapter_record = table_adapter.to_data_set_record()
            data_sets[key] = table_adapter_record.size
        return data_sets

    def set_data_sets_as_dict(self) -> Optional[List[UUID]]:

        dataset_ids = list()

        rows = self.get_tables_from_sql()
        if rows is None:
            return None

        self.tables_table = TableAdapter(self.database_connection)
        if not self.get_tables_table(rows):
            self.tables_table.from_existing_table("initial_table", "initial_table", uuid4())
            self.tables_table.query_sql(SQLQueries.CREATETABLE.value.format(tablename=TABLES_TABLE,
                                                                            columns="table_name TEXT, table_uuid TEXT, "
                                                                                    "table_size DOUBLE PRECISION"),
                                        False)
        else:
            self.tables_table = TableAdapter(self.database_connection)
            self.tables_table.from_existing_table("initial_table", "initial_table", uuid4())

        table_data = self.tables_table.query_sql(SQLQueries.SELECT_FROM.value.format(columns=("table_name" +
                                                                                              "," +
                                                                                              "table_uuid" + "," +
                                                                                              "table_size"),
                                                                                     tablename="{tablename}"))

        if table_data is None:
            if len(self.tables_table.get_errors()) > 0:
                self.throw_error(self.tables_table.get_errors()[0].error_type, self.tables_table.get_errors()[0].args)
            return []
        table_data = table_data.data

        for i, (name, key, size) in table_data[["table_name", "table_uuid", "table_size"]].iterrows():
            uuid = uuid4()
            table_adapter = TableAdapter(self.database_connection)
            table_adapter.from_existing_table(name=name, key=key, uuid=uuid, size=size)
            self.table_adapters[uuid] = table_adapter
            dataset_ids.append(table_adapter.uuid)

        # Add othter datasets and mark them
        for key, size in rows:
            if key != TABLES_TABLE:
                uuid = uuid4()
                self.table_adapters[uuid] = TableAdapter(self.database_connection)
                self.table_adapters[uuid].from_existing_table(name=INVALID_PREFIX + key, key=key, uuid=uuid4(),
                                                              size=size)
                dataset_ids.append(uuid)

        return dataset_ids

    def get_tables_from_sql(self) -> Optional[List[Tuple[str, int]]]:
        try:
            database_connection = self.database_connection.get_connection()
        except DatabaseConnectionError as e:
            self.throw_error(ErrorMessage.DATABASE_CONNECTION_ERROR, ErrorMessage.DETAIL_MESSAGE.value + str(e.args))
            return None
        query = SQLQueries.GET_TABLES_WITH_SIZE.value
        log_query(query)
        cursor = database_connection.execute(text(query))

        rows = cursor.fetchall()
        cursor.close()
        tables = []
        for name, size in rows:
            tables.append((name, size))
        return tables

    def get_columns(self, table_name: str) -> List[str]:
        database_connection = self.database_connection.get_connection()
        cursor = database_connection.execute(text(SQLQueries.GET_COLUMNS.value.format(tablename=table_name)))
        columns = cursor.fetchall()
        cursor.close()
        return columns

    def get_tables_table(self, rows) -> bool:
        for name, size in rows:
            if TABLES_TABLE == name:
                return True
        return False

    def table_exists(self, table_name: str, all_database: bool = False) -> bool:

        tables = self.get_tables_from_sql()


        if all_database:
            return table_name in tables
        for key, value in self.table_adapters.items():
            if value.name == table_name:
                return True
        return False
