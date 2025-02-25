import sqlite3

from core.servertypes import SourceTag

from core.db.sqlitetypes import *





def format_tag(source_tag: SourceTag) -> str:

    return f"{source_tag.device_id}_{source_tag.port}"





class DevicesDatabase:

    def __init__(self, db_path: str) -> None:

        self.db_path = db_path

        self.conn = None

    

    def create_device_tables(self, source_tag: SourceTag) -> None:

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS devices_{format_tag(source_tag)}_integer (source_path TEXT)")

        cursor.execute(f"CREATE TABLE IF NOT EXISTS devices_{format_tag(source_tag)}_real (source_path TEXT)")

        cursor.execute(f"CREATE TABLE IF NOT EXISTS devices_{format_tag(source_tag)}_text (source_path TEXT)")

        cursor.execute(f"CREATE TABLE IF NOT EXISTS devices_{format_tag(source_tag)}_blob (source_path TEXT)")

        self.conn.commit()



    def check_database_exists(self, database: str) -> bool:

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (database,))

        result = cursor.fetchone()

        self.conn.close()

        return result is not None

    

    def get_device_sources(self, source_tag: SourceTag, source_type: sqlite3_type) -> list[str]:

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        _type = str(source_type).lower()

        if not _type in ['blob', 'text', 'integer', 'real']:

            raise ValueError(f"Invalid source type: {_type}")

        cursor.execute(f"SELECT source_path FROM devices_{source_tag.to_string()}_{_type}")

        rows = cursor.fetchall()

        self.conn.close()



        return [row[0] for row in rows]

    



    def add_device_source(self, source_tag: SourceTag, source_path: str, source_type: sqlite3_type) -> None:

        if not self.check_database_exists("devices_{}".format(format_tag(source_tag))):

            self.create_device_tables(source_tag)

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        _type = source_type.__str__().lower()

        if not _type in ['blob', 'text', 'integer', 'real']:

            raise ValueError(f"Invalid source type: {_type}")

        query = f"INSERT INTO devices_{format_tag(source_tag)}_{_type} (source_path) VALUES (?)"

        params = (source_path,)

        cursor.execute(query, params)

        

        self.conn.commit()

        self.conn.close()



        return

    

    def remove_device_source(self, source_tag: SourceTag, source_path: str, source_type: sqlite3_type) -> None:

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        _type = str(source_type).lower()

        if not _type in ['blob', 'text', 'integer', 'real']:

            raise ValueError(f"Invalid source type: {_type}")

        cursor.execute(f"DELETE FROM devices_{source_tag.to_string()}_{str(source_type).lower()} WHERE source_path=?", (source_path,))

        self.conn.commit()

        self.conn.close()



        return

    

    def get_device_sources(self, source_tag: SourceTag, source_type: sqlite3_type) -> list[str]:

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        _type = str(source_type).lower()

        if not _type in ['blob', 'text', 'integer', 'real']:

            raise ValueError(f"Invalid source type: {_type}")

        cursor.execute(f"SELECT source_path FROM devices_{source_tag.to_string()}_{_type}")

        rows = cursor.fetchall()

        self.conn.close()



        return [row[0] for row in rows]

    

