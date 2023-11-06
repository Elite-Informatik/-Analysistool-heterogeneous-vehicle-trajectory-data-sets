from enum import Enum


class SQLQueries(Enum):
    """
    holds all sql queries information_schema.tables
    """

    SELECT_DATASET_METADATA = """
                                SELECT {columns}
                                FROM "{meta_table_name}"
                                WHERE uuid='{uuid}'
                                """
    GET_ALL_TABLES = """
                                 SELECT
                                     tablename
                                 FROM
                                     pg_catalog.pg_tables
                                WHERE
                                    schemaname = 'public'
                    """
    CREATE_TABLE = """
                         CREATE TABLE "{table_name}" ({columns})
                         """
    DELETE_DATASET = """DELETE FROM '{table_name}' WHERE {column}='{uuid}'"""
    GET_DATASET = """
                    SELECT * FROM '{table_name}'
                    WHERE {column}='{uuid}'
                    """
    GET_COLUMN_FROM_TABLE = """
                            SELECT {column} FROM '{table_name}'
                            """
    NOT = "NOT({filter})"
    SELECT_FROM_DATASET = "SELECT {columns} FROM {tablename} WHERE {dataset_column} IN ({dataset_uuids})"
    SELECT_DISTINCT_FROM_DATASET = "SELECT DISTINCT {columns} FROM {tablename} WHERE {dataset_column} " \
                                   "IN ({dataset_uuids})"
    WHERE = " WHERE {filter}"
    AND_IN = " AND {column} IN ({values})"
    AND = " AND {filter}"
    WHERE_FROM_DATASET = "WHERE {dataset_column} in ({dataset_uuids})"
    UPDATE_DATASET_SIZE = "UPDATE '{meta_table_name}' SET {column} = {new_size} WHERE {uuid_column} = '{dataset_uuid}'"
