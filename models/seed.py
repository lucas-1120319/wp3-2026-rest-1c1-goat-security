import sqlite3
from data.database import Database
from models.user import User

class Seed:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def create_row_teacher(self):
        """ Create a new row teacher """
        with self.db.connect() as con:
            cur = con.cursor()

            users = [
                {"first_name": "Henk", "last_name": "Spaans", "email": "henk@mail.nl",
                 "phone": "0123456789", "role_id": 3},
                {"first_name": "Frits", "last_name": "Fristie", "email": "frits@mail.nl",
                 "phone": "0123456789", "role_id": 3}
            ]

            # Create Users
            for user in users:
                cur.execute(
                    "INSERT OR IGNORE INTO users (email, phone, password, role_id) "
                    "VALUES (?, ?, ?, ?)",
                    (user['email'], user['phone'], User.hash_password('secret'), user['role_id']),
                )

                cur.execute(
                    "SELECT id FROM users WHERE email = ?",
                    (user['email'],)
                )
                user_id = cur.fetchone()[0]

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

    def assign_teacher_group(self):
        """ Assign teacher group to students """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT id FROM teachers "
                "WHERE first_name = 'Henk' AND last_name = 'Spaans' ",
            )
            henk = cur.fetchone()

            cur.execute(
                "SELECT id FROM teachers "
                "WHERE first_name = 'Frits'",
            )
            frits = cur.fetchone()

            cur.execute("SELECT id FROM studentGroups WHERE name = '1c'")
            group_b = cur.fetchone()

            cur.execute("SELECT id FROM studentGroups WHERE name = '1a'")
            group_a = cur.fetchone()
            cur.execute(
                "INSERT OR IGNORE INTO teacher_studentGroup (studentGroup_id, teacher_id)"
                "VALUES (?, ?)",
                (group_a["id"], henk['id'])
            )

            cur.execute(
                "INSERT OR IGNORE INTO teacher_studentGroup (studentGroup_id, teacher_id)"
                "VALUES (?, ?)",
                (group_b["id"], frits['id'])
            )
            con.commit()



    def add_students_in_group(self):
        """ Add students to a group """
        with self.db.connect() as con:
            cur = con.cursor()

            studentGroups = ["1a", "1c"]

            # Get all students
            cur.execute("SELECT id FROM students")
            student_rows = cur.fetchall()

            if not student_rows:
                print("No students found.")
                return

            # Split students in half
            half = len(student_rows) // 2
            first_half = student_rows[:half]
            second_half = student_rows[half:]# Loop through each group and assign students
            for index, group_name in enumerate(studentGroups):

                # Get group ID
                cur.execute("SELECT id FROM studentGroups WHERE name = ?", (group_name,))
                group_row = cur.fetchone()

                if not group_row:
                    print(f"Group '{group_name}' does not exist")
                    continue

                group_id = group_row[0]

                # Decide which students belong to this group
                if index == 0:
                    assigned_students = first_half
                else:
                    assigned_students = second_half

                # Insert into relation table
                for student in assigned_students:
                    student_id = student[0]
                    cur.execute(
                        "INSERT OR IGNORE INTO student_studentGroups (student_id, studentGroup_id) "
                        "VALUES (?, ?)",
                        (student_id, group_id)
                    )

            # Commit once at the end (better performance)
            con.commit()

    def assign_class_subjects(self):
        """ Connect classes to subjects """
        with self.db.connect() as con:
            cur = con.cursor()

            cur.execute("DELETE FROM studentGroup_subjects") # CLEAR EXISTING TABLE

            cur.execute("SELECT id, name FROM studentGroups")
            groups = cur.fetchall()

            cur.execute("SELECT id, external_id, name FROM subjects")
            subjects = cur.fetchall()

            for group_id, _group_name in groups:
                for subject_id, _ext_id, _subj_name in subjects:
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO studentGroup_subjects (studentGroup_id, subject_id)
                        VALUES (?, ?)
                        """,
                        (group_id, subject_id),
                    )
