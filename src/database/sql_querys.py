from enum import Enum


class SQLQueries(Enum):
    """
    holds all sql queries
    """

    # CREATETABLE = """
    #                 CREATE TABLE "{tablename}" ({columns})
    #                 """
    # DROPTABLE = "DROP TABLE {tablename};"
    # SELECT = "SELECT {columns}"
    # FROM = " FROM {tablename} AS t"
    # WHERE = " WHERE {filter}"
    # SELECT_FROM = "SELECT {columns} FROM {tablename}"
    # SELECTFILTERED = "SELECT {columns} FROM {tablename} WHERE {filter}"
    # NOT = "NOT({filter})"
    # SELECTGROUPEDFILTERED = "SELECT {data} FROM {tablename} WHERE {filter} GROUP BY {data}"
    # GROUPED = " GROUP BY {columns}"
    # WHEREIN = " WHERE {column} IN ({values})"
    # SELECTINFILTERED = "SELECT {columns} FROM {tablename} WHERE {data} IN ({values}) AND {filter}"
    # INSERT = "INSERT INTO {tablename} VALUES {values}"
    # GET_COLUMNS = "SELECT column_name FROM information_schema.columns WHERE table_name = '{tablename}'"
    # GET_ALL_TABLES = """
    #                         SELECT
    #                             table_name
    #                         FROM
    #                             information_schema.tables
    #                         WHERE
    #                             table_schema = 'public';
    #                         """
    # GET_TABLES_FROM_TABLE_WITH_SIZE = """
    #                         SELECT name, size
    #                         FROM "{tablename}"
    #                         """
    # GET_TABLES_FROM_TABLE = """
    #                         SELECT DISTINCT name
    #                         FROM "{tablename}"
    #             """
    # TABLE_SIZE = """SELECT
    #                     pg_total_relation_size(quote_ident(table_name)) / 1024 / 1024 AS size_in_mb
    #                 FROM
    #                     information_schema.tables
    #                 WHERE
    #                     table_name='{tablename}'
    #                 LIMIT 1
    #                 """
    # UPDATE = """UPDATE {tablename}
    #             SET {update_columns}
    #             WHERE {key_column}"""
    # DELETE = """DELETE FROM {tablename}
    #             WHERE {key_column}"""
    # SELECT_UUID_FROM_TABLE = """SELECT uuid FROM "{meta_table_name}" WHERE name='{tablename}'"""

    SELECT_DATASET_METADATA = """
                                SELECT {columns}
                                FROM "{meta_table_name}"
                                WHERE uuid='{uuid}'
                                """
    GET_ALL_TABLES = """
                                 SELECT
                                     '{table_name}'
                                 FROM
                                     information_schema.tables
                                 WHERE
                                     table_schema = 'public';
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
