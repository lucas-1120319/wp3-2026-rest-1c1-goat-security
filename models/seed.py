import sqlite3
from data.database import Database

class Seed:
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


    def create_student_group(self):
        """ Create a new student group/class """
        with self.db.connect() as con:
            cur = con.cursor()
            groups = ['1a', '1b', '1c', '1d']
            for group in groups:
                cur.execute(
                    "INSERT OR IGNORE INTO studentGroups (name)"
                    "VALUES (?)",
                    (group,)
                )
            con.commit()


    def create_row_student(self):
        """ Create a new row student """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT id FROM users WHERE role_id = 2",
            )
            student_ids = cur.fetchall()

            for student in student_ids:
                student_id = student[0]
                print("student_id:", student_id)
                cur.execute(
                    "INSERT OR IGNORE INTO students (user_id)" 
                    "VALUES(?) ",
                    (student_id,)
                )
            con.commit()


    def add_students_in_group(self, group_name):
        """ Add students to a group """
        with self.db.connect() as con:
            cur = con.cursor()

            # Get ID form group
            cur.execute("SELECT id FROM studentGroups WHERE name = ?", (group_name,))
            group_row = cur.fetchone()

            if not group_row:
                print("group does not exist")
                return

            group_id = group_row[0]

            # get id from students
            cur.execute("SELECT id FROM students")
            student_rows = cur.fetchall()

            # Add both items together in teh table
            for student in student_rows:
                student_id = student[0]
                cur.execute(
                    "INSERT OR IGNORE INTO student_studentGroups (student_id, studentGroup_id) "
                    "VALUES (?, ?)",
                    (student_id, group_id)
                )

