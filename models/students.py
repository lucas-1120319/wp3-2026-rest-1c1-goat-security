import sqlite3
from data.database import Database
from router.student_route import student_bp


class Student:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def get_all_student_user_info(self, user_id: int):
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT user_id, email, phone, first_name, last_name, postcode, gender, city, country, street_name, birth_date FROM students inner join users ON students.user_id = users.id WHERE user_id = ?""", (user_id,))
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

    def get_learning_goals(self, subject_id: int):
        """ Get list of learning goals of DB """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT id, title FROM learningGoals WHERE subject_id = ?""", (subject_id,))
            return cur.fetchall()


    def get_learning_goals_title(self, subject_id: int):
        """ Get title of the learning goal. """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute(
                "SELECT lg.id AS lg_id, title, name FROM learningGoals lg JOIN subjects ON lg.subject_id = subjects.id "
                "WHERE subject_id = ?", (subject_id,))
            return cur.fetchone()

    def get_snapshot_by_learning_goal_id(self, learning_goal_id: int, student_id: int):
        """ Get exam result data by snapshot id """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(
                "SELECT tax.id AS tax_id, " 
                "tax.level AS tax_level, "
                "tax.kennen AS tax_kennen, "
                "tax.kunnen AS tax_kunnen, "
                "tax.confidence AS tax_confidence, "
                "tax.snapshot_id AS tax_snap, "
                "tax.student_id AS tax_student_id, "

                "snap.at AS snap_at, "

                "lg.external_id AS lg_external_id, "
                "lg.title AS lg_title "

                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "WHERE snap.learningGoal_id = ? AND tax.student_id = ? ",
                (learning_goal_id, student_id)
            )
            return cur.fetchall()

    def get_snapshot(self, snapshot_id: int, student_id: int):
        """ Get exam result data by snapshot id """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT tax.id AS tax_id, "
                "tax.level AS tax_level, "
                "tax.kennen AS tax_kennen, "
                "tax.kunnen AS tax_kunnen, "
                "tax.confidence AS tax_confidence, "
                "tax.snapshot_id AS tax_snap, "
                "tax.student_id AS tax_student_id, "

                "snap.at AS snap_at, "

                "lg.external_id AS lg_external_id, "
                "lg.title AS lg_title "

                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "WHERE tax.snapshot_id = ? AND tax.student_id = ? ",
                (snapshot_id, student_id)
            )
            return cur.fetchall()

    def get_snapshot_title(self, snapshot_id: int, student_id: int):
        """ Get exam result data by snapshot id with title of subject"""
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT tax.id AS tax_id, "
                "tax.level AS tax_level, "
                "tax.kennen AS tax_kennen, "
                "tax.kunnen AS tax_kunnen, "
                "tax.confidence AS tax_confidence, "
                "tax.snapshot_id AS tax_snap, "
                "tax.student_id AS tax_student_id, "

                "snap.at AS snap_at, "

                "lg.external_id AS lg_external_id, "
                "lg.title AS lg_title "

                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "WHERE tax.snapshot_id = ? AND tax.student_id = ? ",
                (snapshot_id, student_id)
            )
            return cur.fetchone()


    def get_exam_list(self, learning_goal_id: int, student_id: int):
        """ Get exam result data by snapshot id """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(
                "SELECT DISTINCT tax.id AS tax_id, " 
                "tax.level AS tax_level, "
                "tax.kennen AS tax_kennen, "
                "tax.kunnen AS tax_kunnen, "
                "tax.confidence AS tax_confidence, "
                "tax.snapshot_id AS tax_snap, "
                "tax.student_id AS tax_student_id, "

                "snap.at AS snap_at, "
                
                "src.type AS src_type, "
                "src.external_id AS src_exid, "

                "lg.external_id AS lg_external_id, "
                "lg.title AS lg_title "

                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN sources src ON snap.source_id = src.id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "WHERE snap.learningGoal_id = ? AND tax.student_id = ? "
                "GROUP BY snap.at ",
                (learning_goal_id, student_id)
            )
            return cur.fetchall()
