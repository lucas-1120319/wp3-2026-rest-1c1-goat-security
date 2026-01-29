import sqlite3
from data.database import Database


class Teacher:
    def __init__(self, db_path: str):
        self.db = Database(db_path)


    # make your own methods