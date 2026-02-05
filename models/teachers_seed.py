import sqlite3
from data.database import Database

class Teacher:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def create_row_teacher(self):
        """ Create a new row teacher """
        with self.db.connect() as con:
            cur = con.cursor()

            users = [
                {"first_name": "Nina", "last_name": "Barak", "email": "nina@mail.nl", "phone": "0123456789", "role_id": 2},
                {"first_name": "Kees", "last_name": "Sterk", "email": "kees@mail.nl", "phone": "0123456789", "role_id": 2},
                {"first_name": "Henk", "last_name": "Spaans", "email": "henk@mail.nl", "phone": "0123456789", "role_id": 3},
                {"first_name": "Frits", "last_name": "Fristie", "email": "frits@mail.nl", "phone": "0123456789", "role_id": 3}
            ]

            # Create Users
            for user in users:
                cur.execute(
                    "INSERT OR IGNORE INTO users (email, phone, password, role_id) VALUES (?, ?, ?, ?)",
                    (user['email'], user['phone'], 'secret', user['role_id']),
                )

                cur.execute(
                    "SELECT id FROM users WHERE email = ?",
                    (user['email'],)
                )
                user_id = cur.fetchone()[0]
                print("user_id:", user_id)

                # Create teacher
                if user["role_id"] == 3:
                    cur.execute(
                        "INSERT OR IGNORE INTO teachers (user_id, first_name, last_name)"
                        "VALUES (?, ?, ?)",
                        (user_id, user['first_name'], user['last_name'])
                    )
            con.commit()

