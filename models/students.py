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



    # def get_snapshot_by_id(self, snapshot_id:int, student_id:int):
    #     with self.db.connect() as con:
    #         con.row_factory = sqlite3.Row
    #         cur = con.cursor()
    #         cur.execute(
    #             "SELECT student_id, snapshot_id FROM taxonomies "
    #             "WHERE snapshot_id = ? AND student_id = ?",
    #             (snapshot_id, student_id)
    #         )
    #         return cur.fetchall()


    def get_snapshot_by_id(self, snapshot_id: int, student_id: int):
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
                "lg.title AS lg_title, "

                "sub.name AS lg_title "

                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "JOIN subjects sub ON sub.id = lg.id "
                "WHERE tax.snapshot_id = ? AND tax.student_id = ? ",
                (snapshot_id, student_id)
            )
            return cur.fetchall()
