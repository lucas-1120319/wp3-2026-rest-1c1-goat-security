import sqlite3
from data.database import Database
import json

class data_converter:
    def __init__(self, db_path: str, json_path: str):
        self.db = Database(db_path)
        self.json_path = json_path

        self.load_data()

    def load_data(self):
        json_path = self.json_path
        with self.db.connect() as con:
            cur = con.cursor()

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for entry in data["entries"]:
            student = entry["student"]

            email = f"{student['name'].lower()}@example.com"
            password = "geheim"
            role_id =  2 # student in database

            # Insert into users

            cur.execute(
                "INSERT OR IGNORE INTO users (email, password, role_id ) VALUES (?, ? , ? )",
                (email, password, role_id,)
            )



            user_id = cur.lastrowid  # get the PK
            cur.execute("INSERT OR IGNORE INTO students (user_id, external_id, first_name) VALUES (?,?, ?)", (user_id, student["id"], student["name"],))
            print(student)
        con.commit()