import sqlite3
from data.database import Database


class Teacher:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def get_teacher_id(self, user_id: int):
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT id
                           FROM teachers
                           WHERE user_id = ?""", (user_id,))
            return cur.fetchone()

    def get_all_teacher_user_info(self, user_id: int):
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT email,
                                  phone,
                                  first_name,
                                  last_name,
                                  postcode,
                                  gender,
                                  city,
                                  country,
                                  street_name,
                                  birth_date
                           FROM teachers
                                    inner join users ON teachers.user_id = users.id
                           WHERE user_id = ?""", (user_id,))
            return cur.fetchone()

    def update_profile(self, user_id: int, data: dict):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""UPDATE teachers
                           Set first_name  = ?,
                               last_name   = ?,
                               postcode    = ?,
                               gender      = ?,
                               city        = ?,
                               country     = ?,
                               street_name = ?,
                               birth_date  = ?
                           WHERE user_id = ?""",
                        (data["first_name"], data["last_name"], data["postcode"], data["gender"], data["city"],
                         data["country"], data["street_name"], data["birth_date"], user_id,))
            con.commit()
            cur.execute("""UPDATE users
                           Set email    = ?,
                               phone    = ?,
                               password = ?
                           WHERE id = ?""",
                        (data["email"], data["phone"], data["password"], user_id,))
            con.commit()

            return cur.fetchone()

    def get_studentGroups(self, teacher_id: int):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT studentGroups.name, studentGroups.id FROM teacher_studentGroup "
                        "INNER JOIN studentGroups ON studentGroups.id = teacher_studentGroup.studentGroup_id "
                        "WHERE teacher_id = ? ",
                        (teacher_id,))
            con.commit()
            return cur.fetchall()

    def get_all_studentGroups(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT studentGroups.name, studentGroups.id FROM studentGroups",)
            con.commit()
            return cur.fetchall()

    def get_all_students_studentGroup(self, class_id: int):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT 
                    students.id,
                    students.first_name,
                    students.last_name,
                    students.postcode,
                    students.gender,
                    students.city,
                    students.country,
                    students.street_name,
                    students.birth_date,
                    (AVG(taxonomies.kennen) + AVG(taxonomies.kunnen)) / 2.0 AS average,
                    AVG(taxonomies.confidence) AS avg_confidence
                FROM students
                INNER JOIN student_studentGroups ON students.id = student_studentGroups.student_id
                INNER JOIN studentGroups ON studentGroups.id = student_studentGroups.studentGroup_id
                INNER JOIN taxonomies ON students.id = taxonomies.student_id
                WHERE studentGroups.name = ?
                GROUP BY students.id
                ORDER BY students.id ASC
                """,
                (class_id,),
            )
            con.commit()
            return cur.fetchall()

    def get_all_subjects(self):
        """ Get all subjects. """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT subjects.name, subjects.id FROM subjects "
                # "JOIN learningGoals ON subjects.id = learningGoals.subject_id "
            )
        return cur.fetchall()

    def get_all_learning_goals(self, subject_id):
        """ Get learning goals. """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT learningGoals.title FROM subjects "
                "JOIN learningGoals ON subjects.id = learningGoals.subject_id "
                "WHERE subjects.id = ? ",
                (subject_id, )
            )
            return cur.fetchall()

    def get_single_subject(self, subject_id):
        """ Get single subject. """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT subjects.name FROM subjects "
                "WHERE subjects.id = ? ",
                (subject_id, )
            )
            return cur.fetchone()



    # def get_learning_goals_list(self):
    #     """ Get keyword and taxonomy score for group. """
    #     with self.db.connect() as con:
    #         cur = con.cursor()
    #         cur.execute(
    #             """
    #             SELECT st.id,
    #                 st.first_name AS st_name,
    #                 lg.title AS lg_title,
    #                 lg.id AS lg_id,
    #                 tax.level AS tax_level,
    #                 tax.kennen AS tax_kennen,
    #                 tax.kunnen  AS tax_kunnen
    #
    #             FROM students st
    #                 LEFT JOIN student_studentGroups ssg ON st.id = ssg.student_id
    #                 LEFT JOIN studentGroups sg ON sg.id = ssg.studentGroup_id
    #                 LEFT JOIN studentGroup_subjects sgs ON ssg.studentGroup_id = sgs.studentGroup_id
    #                 LEFT JOIN taxonomies tax ON st.id = tax.student_id
    #                 LEFT JOIN learningGoals lg ON sgs.subject_id = lg.subject_id
    #                 INNER JOIN learningGoal_keywords ON learningGoal_keywords.learningGoal_id = lg.id
    #                 INNER JOIN keywords key ON learningGoal_keywords.keyword_id = key.id
    #                 INNER JOIN snapshots ss ON ss.learningGoal_id = lg.id
    #
    #                 GROUP BY lg.title
    #                 ORDER BY lg.id
    #
    #             """,
    #         )
    #         return cur.fetchall()


# Controleren of deze werkt of niet ?
    def get_exam_list(self, subject_id):
        """ Get learning goals. """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT learningGoals.title FROM subjects "
                "JOIN learningGoals ON subjects.id = learningGoals.subject_id "
                "WHERE subjects.id = ? and tax.snap",
                (subject_id, )
            )
            return cur.fetchall()