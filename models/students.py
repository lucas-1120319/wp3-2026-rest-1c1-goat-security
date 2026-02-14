import sqlite3
from data.database import Database


class Student:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def get_all_student_user_info(self, user_id: int):
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT email, phone, first_name, last_name, postcode, gender, city, country, street_name, birth_date FROM students inner join users ON students.user_id = users.id WHERE user_id = ?""", (user_id,))
            return cur.fetchone()

    def get_student_class(self, user_id):
        """ get the current student's class """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM students INNER JOIN student_studentGroups "
                "ON students.id = student_studentGroups.student_id INNER JOIN studentGroups "
                "ON studentGroups.id = student_studentGroups.studentGroup_id WHERE students.user_id = ?",
                (user_id,),
            )
            con.commit()
            return cur.fetchone()

    def get_all_subjects_students(self, class_id):
        """ get all subjects from a class """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM subjects INNER JOIN studentGroup_subjects "
                "ON subjects.id = studentGroup_subjects.subject_id INNER JOIN studentGroups "
                "ON studentGroups.id = studentGroup_subjects.studentGroup_id WHERE studentGroups.name = ?",
                (class_id,),
            )
            con.commit()
            return cur.fetchall()

    def update_profile(self,user_id: int, data: dict ):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""UPDATE students Set first_name = ?, last_name = ?, postcode = ?, gender = ?, city = ?, country = ?, street_name = ?, birth_date = ? WHERE user_id = ?""",
                        (data["first_name"], data["last_name"], data["postcode"], data["gender"], data["city"],data["country"], data["street_name"], data["birth_date"], user_id,))
            con.commit()
            cur.execute("""UPDATE users
                           Set email = ? ,
                               phone = ?,
                               password = ?
                           WHERE id = ?""",
                        (data["email"], data["phone"], data["password"],user_id, ))
            con.commit()

            return cur.fetchone()
