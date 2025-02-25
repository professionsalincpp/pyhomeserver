import dataclasses

from typing import List, Union

import warnings

import sqlite3





class INTEGER(int):

    """Integer value."""

    @classmethod

    def __str__(cls):

        return "INTEGER"

    



class REAL(float):

    """Real number value."""

    @classmethod

    def __str__(cls):

        return "REAL"

    



class TEXT(str):

    """String value."""

    @classmethod

    def __str__(cls):

        return "TEXT"



class BLOB(bytes):

    """Binary data value."""

    @classmethod

    def __str__(cls):

        return "BLOB"





sqlite3_type = Union[INTEGER, REAL, TEXT, BLOB]





@dataclasses.dataclass

class Column:

    name: str

    type: sqlite3_type

    primary_key: bool = False







@dataclasses.dataclass

class Table:

    name: str

    columns: List[Column]

    def __post_init__(self):

        self.primary_key_column = 0

        _is_primary_key_finded = False

        for i, column in enumerate(self.columns):

            if column.primary_key:

                if _is_primary_key_finded:

                    warnings.warn("More than one primary key in table {}, Used the first one".format(self.name))

                self.primary_key_column = i

                _is_primary_key_finded = True



    def create_table_sql(self) -> str:

        sql = "CREATE TABLE IF NOT EXISTS {} (".format(self.name)

        for i, column in enumerate(self.columns):

            sql += column.name + " " + column.type.__str__()

            if i == self.primary_key_column:

                sql += " PRIMARY KEY"

            if i < len(self.columns) - 1:

                sql += ", "

        sql += ");"

        print(sql)

        return sql

            



class DataBase:

    def __init__(self, db_path: str):

        self.db_path = db_path

        self.tables: List[Table] = []

    

    def add_table(self, table: Table):

        self.tables.append(table)



    def table_exists(self, table: Table):

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table.name,))

        result = cursor.fetchone()

        conn.close()

        return result is not None

    

    def drop_table(self, table: Table):

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS {}".format(table.name))

        conn.commit()

        conn.close()



        self.tables.remove(table)



        return True

    

    def create_table(self, table: Table):

        if self.table_exists(table):

            return False

        self.tables.append(table)

        return True





    def create_tables(self):

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()

        for table in self.tables:

            cursor.execute(table.create_table_sql())

        conn.commit()

        conn.close()

    

    def close(self):

        conn = sqlite3.connect(self.db_path)

        conn.close()



    def __enter__(self):

        self.create_tables()



        return self

    

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.close()



        return False

    

    def execute_query(self, query: str, params=None) -> List:

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()

        cursor.execute(query, params)

        result = cursor.fetchall()

        conn.commit()

        conn.close()



        return result

