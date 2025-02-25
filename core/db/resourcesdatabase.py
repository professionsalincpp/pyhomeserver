import sqlite3

from typing import overload

from core.servertypes import SourceId

from .sqlitetypes import *





class ResourceDatabase(DataBase):

    integer_table = Table(name="integer", columns=[

                    Column(name="name", type=TEXT, primary_key=True),

                    Column(name="value", type=INTEGER)])

    float_table = Table(name="float", columns=[

                    Column(name="name", type=TEXT, primary_key=True),

                    Column(name="value", type=REAL)])

    text_table = Table(name="text", columns=[

                    Column(name="name", type=TEXT, primary_key=True),

                    Column(name="value", type=TEXT)])

    blob_table = Table(name="blob", columns=[

                    Column(name="name", type=TEXT, primary_key=True),

                    Column(name="value", type=BLOB)])

    def __init__(self, db_path: str) -> None:

        super().__init__(db_path)

        self.tables = [

            ResourceDatabase.integer_table,

            ResourceDatabase.float_table,

            ResourceDatabase.text_table,

            ResourceDatabase.blob_table

        ]

        self.create_tables()



    @overload

    def store(self, id: SourceId, value: int) -> bool: ...

    @overload

    def store(self, id: SourceId, value: float) -> bool: ...

    @overload

    def store(self, id: SourceId, value: str) -> bool: ...

    @overload

    def store(self, id: SourceId, value: bytes) -> bool: ...

    def store(self, id: SourceId, value: Union[int, float, str, bytes]) -> bool:

        if isinstance(value, int):

            return self.store_integer(id, value)

        if isinstance(value, float):

            return self.store_float(id, value)

        if isinstance(value, str):

            return self.store_text(id, value)

        if isinstance(value, bytes):

            return self.store_blob(id, value)

        return False

    

    def store_integer(self, id: SourceId, value: int) -> bool:

        # Check for an existing value in the database

        result = self.execute_query("SELECT value FROM {} WHERE name =?".format(ResourceDatabase.integer_table.name), (id.to_string(),))



        if result is not None and len(result) > 0:

            self.execute_query("UPDATE {} SET value =? WHERE name =?".format(ResourceDatabase.integer_table.name), (value, id.to_string()))



        # Insert the new value into the database

        self.execute_query("INSERT INTO {} (name, value) VALUES (?,?)".format(ResourceDatabase.integer_table.name), (id.to_string(), value))



        return True

    

    def store_float(self, id: SourceId, value: float) -> bool:

        result = self.execute_query("SELECT value FROM {} WHERE name =?".format(ResourceDatabase.float_table.name), (id.to_string(),))

        

        if result is not None and len(result) > 0:

            self.execute_query("UPDATE {} SET value =? WHERE name =?".format(ResourceDatabase.float_table.name), (value, id.to_string()))



        # Insert the new value into the database

        self.execute_query("INSERT INTO {} (name, value) VALUES (?,?)".format(ResourceDatabase.float_table.name), (id.to_string(), value))



        return True

    

    def store_text(self, id: SourceId, value: str) -> bool:

        result = self.execute_query("SELECT value FROM {} WHERE name =?".format(ResourceDatabase.text_table.name), (id.to_string(),))

        

        if result is not None and len(result) > 0:

            self.execute_query("UPDATE {} SET value =? WHERE name =?".format(ResourceDatabase.text_table.name), (value, id.to_string()))



        # Insert the new value into the database

        self.execute_query("INSERT INTO {} (name, value) VALUES (?,?)".format(ResourceDatabase.text_table.name), (id.to_string(), value))



        return True

    

    def store_blob(self, id: SourceId, value: bytes) -> bool:

        result = self.execute_query("SELECT value FROM {} WHERE name =?".format(ResourceDatabase.blob_table.name), (id.to_string(),))



        if result is not None and len(result) > 0:

            self.execute_query("UPDATE {} SET value =? WHERE name =?".format(ResourceDatabase.blob_table.name), (value, id.to_string()))



        # Insert the new value into the database

        self.execute_query("INSERT INTO {} (name, value) VALUES (?,?)".format(ResourceDatabase.blob_table.name), (id.to_string(), value))

        

        return True

    

    def retrieve(self, id: SourceId) -> Union[int, float, str, bytes, None]:

        result = self.execute_query("SELECT value FROM {} WHERE name = ?".format(ResourceDatabase.integer_table.name), (id.to_string(),))

        if result is not None and len(result) > 0:

            return result[0][0]

        result = self.execute_query("SELECT value FROM {} WHERE name = ?".format(ResourceDatabase.float_table.name), (id.to_string(),))

        if result is not None and len(result) > 0:

            return result[0][0]

        result = self.execute_query("SELECT value FROM {} WHERE name = ?".format(ResourceDatabase.text_table.name), (id.to_string(),))

        if result is not None and len(result) > 0:

            return result[0][0]

        result = self.execute_query("SELECT value FROM {} WHERE name = ?".format(ResourceDatabase.blob_table.name), (id.to_string(),))

        if result is not None and len(result) > 0:

            return result[0][0]

        return None

    

    def delete(self, id: SourceId) -> bool:

        self.execute_query("DELETE FROM {} WHERE name = ?".format(ResourceDatabase.integer_table.name), (id.to_string(),))

        self.execute_query("DELETE FROM {} WHERE name = ?".format(ResourceDatabase.float_table.name), (id.to_string(),))

        self.execute_query("DELETE FROM {} WHERE name = ?".format(ResourceDatabase.text_table.name), (id.to_string(),))

        self.execute_query("DELETE FROM {} WHERE name = ?".format(ResourceDatabase.blob_table.name), (id.to_string(),))

        return True



    

