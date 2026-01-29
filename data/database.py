import sqlite3
class Database:
    def __init__(self, path: str):
        self.path = path
        self._setup_tables()

    def connect(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _setup_tables(self):
        with self.connect() as con:
            cur = con.cursor()

            # Put your own queries here.

            con.commit()