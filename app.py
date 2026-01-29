import os
from data.database import Database

print("Hello world")

#make the default path for the database
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")


_db = Database(DB_PATH)