from typing import List
from typing import Optional

from src.data_transfer.content.column import Column
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import DataRecord
from src.database.data_facade import DataFacade
from src.database.sql_querys import SQLQueries
from src.database.table_adapter import TableAdapter


class PostgreSQLDataFacade(DataFacade):
    """
    Postgre Adapter for the database
    """
    table_adapter: Optional[TableAdapter]

    def __init__(self):
        super().__init__()
        self.use_trajectory_filter = None
        self.trajecotry_filter = None
        self.use_filter = None
        self.filter = None
        self.table_adapter = None

    def set_table_adapter(self, table_adapter: TableAdapter):
        """
        sets the table adapter
        :param table_adapter: the table adapter
        """
        self.table_adapter = table_adapter

    def check_table_adapter(self):
        """
        checks whether the table adapter is None
        """
        if self.table_adapter is None:
            raise RuntimeError("Dataset can't be accessed before opening an Dataset.")

    def set_point_filter(self, filter_str: str, use_filter: bool, negate_filter: bool) -> None:
        self.check_table_adapter()
        if filter_str is None or filter_str == "":
            self.filter = None
            return None

        if negate_filter:
            self.filter = SQLQueries.NOT.value.format(filter=filter_str)
        else:
            self.filter = filter_str
        self.use_filter = use_filter

    def set_trajectory_filter(self, filter_str: str, use_filter: bool) -> None:
        if filter_str is None or filter_str == "":
            self.trajecotry_filter = None
            return None
        self.check_table_adapter()
        self.trajecotry_filter = filter_str
        self.use_trajectory_filter = use_filter

    def get_data(self, returned_columns: List[Column], usefilter: bool = True) -> Optional[DataRecord]:
        self.check_table_adapter()
        str_columns: List[str] = list()

        for column in returned_columns:
            str_columns.append(column.value)

        query = SQLQueries.SELECT.value.format(columns=", ".join(str_columns))
        query += SQLQueries.FROM.value

        if usefilter is True and self.filter is not None:
            query += SQLQueries.WHERE.value.format(filter=self.filter)

        data = self.table_adapter.query_sql(query)
        if data is None:
            for error in self.table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return None
        return data

    def get_distinct_data_from_column(self, returned_column: Column) -> Optional[DataRecord]:

        self.check_table_adapter()
        query = SQLQueries.SELECT.value.format(columns=returned_column.value) \
                + SQLQueries.FROM.value \
                + SQLQueries.GROUPED.value.format(columns=returned_column.value)
        data = self.table_adapter.query_sql(query)
        if data is None:
            for error in self.table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return None
        return data

    def get_data_of_column_selection(self, returned_columns: List[Column], chosen_elements: List,
                                     chosen_column: Column, usefilter: bool = True) -> Optional[DataRecord]:
        if len(chosen_elements) == 0 or chosen_column is None:
            raise InvalidInput("No elements selected")

        self.check_table_adapter()
        str_columns: List[str] = list()
        for column in returned_columns:
            str_columns.append(column.value)

        query = SQLQueries.SELECT.value.format(columns=", ".join(str_columns))
        query += SQLQueries.FROM.value
        str_values: List[str] = list()
        for value in chosen_elements:
            str_values.append("'" + value.__str__() + "'")

        query += SQLQueries.WHEREIN.value.format(column=chosen_column.value, values=", ".join(str_values))

        if usefilter is True and self.filter is not None:
            query += " and " + self.filter

        data: DataRecord = self.table_adapter.query_sql(query)
        if data is None:
            for error in self.table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return None

        if len(data.data) == 0:
            self.throw_error(ErrorMessage.TRAJECTORY_NOT_EXISTING, msg="No trajectory selected")
            for error in self.table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return None
        return data

    def get_trajectory_ids(self) -> Optional[DataRecord]:
        self.check_table_adapter()
        query = SQLQueries.SELECT.value.format(columns=Column.TRAJECTORY_ID.value)
        query += SQLQueries.FROM.value
        if self.use_trajectory_filter and self.trajecotry_filter is not None:
            query += SQLQueries.WHERE.value.format(filter=self.trajecotry_filter)
        query += SQLQueries.GROUPED.value.format(columns=Column.TRAJECTORY_ID.value)

        trajectory_ids = self.table_adapter.query_sql(query)
        if trajectory_ids is None:
            for error in self.table_adapter.get_errors():
                self.throw_error(error.error_type, error.args)
            return None
        return trajectory_ids
