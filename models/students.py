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
            cur.execute("""SELECT user_id, email, phone, first_name, last_name,  birth_date FROM students inner join users ON students.user_id = users.id WHERE user_id = ?""", (user_id,))
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
            cur.execute("""UPDATE students Set first_name = ?, last_name = ?, birth_date = ? WHERE user_id = ?""",
                        (data["first_name"], data["last_name"], data["birth_date"], user_id,))
            con.commit()

            if data.get("password"):
                cur.execute("""
                    UPDATE users
                    SET email = ?, phone = ?, password = ?
                    WHERE id = ?
                """, (data["email"], data["phone"], data["password"], user_id))
            else:
                cur.execute("""
                    UPDATE users
                    SET email = ?, phone = ?
                    WHERE id = ?
                """, (data["email"], data["phone"], user_id))

            con.commit()
            return cur.fetchone()

    def get_learning_goals(self, subject_id: int):
        """ Get list of learning goals of DB """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT id, title FROM learningGoals WHERE subject_id = ?""", (subject_id,))
            return cur.fetchall()

    def get_learning_goals_filter_keywords(self, subject_id: int, keyword: str):
        """ Get list of learning goals of DB """
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT DISTINCT lg.id, lg.title FROM learningGoals as lg INNER JOIN learningGoal_keywords AS lg_kw ON lg.id = lg_kw.learningGoal_id INNER JOIN keywords ON keywords.id = lg_kw.keyword_id  WHERE subject_id = ? AND keywords.name LIKE ?""", (subject_id,f"%{keyword}%",))
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

    def get_learning_goal(self, learningGoal_id: int):
        with self.db.connect() as con:

            cur = con.cursor()
            cur.execute(
                """
                SELECT learningGoals.title, subjects.name as subject_name
                FROM learningGoals
                         INNER JOIN subjects ON subjects.id = learningGoals.subject_id
                WHERE learningGoals.id = ?
                """,
                (learningGoal_id,)
            )

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

    def get_learning_goals_number_of_results(self, learning_goal_id: int, student_id: int):
        """ Get exam result data by snapshot id """
        with self.db.connect() as con:
            cur = con.cursor()


            cur.execute(
                "SELECT DISTINCT tax.id AS tax_id, "
                "tax.level AS tax_level, "
                "(AVG(tax.kennen) + AVG(tax.kunnen)) / 2.0 AS average "
                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "WHERE snap.learningGoal_id = ? AND tax.student_id = ? "
                "GROUP BY tax.level ",
                (learning_goal_id, student_id)
            )
            all_results = cur.fetchall()
            count = 0
            for row in all_results:
                if row["average"] > 0.5:
                    count += 1

            return count

    def get_result_per_snapshot(self, learning_goal_id: int, student_id: int):
        """ Get exam result data by snapshot id """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT DISTINCT tax.id AS tax_id, "
                "tax.level AS level, "
                "snap.id AS snapshot_id, "
                "sources.external_id AS source_id, "
                "sources.type AS source_type, "
                "ROUND((AVG(tax.kennen) + AVG(tax.kunnen)) / 2.0, 2) AS average, "
                "snap.at AS snap_date "
                "FROM taxonomies tax "
                "JOIN snapshots snap ON tax.snapshot_id = snap.id "
                "JOIN sources ON sources.id = snap.source_id "
                "JOIN learningGoals lg ON snap.learningGoal_id = lg.id "
                "WHERE snap.learningGoal_id = ? AND tax.student_id = ? "
                "GROUP BY snap.at, tax.level",
                (learning_goal_id, student_id)
            )
            all_results = cur.fetchall()
            return all_results

    def learning_goal_keywords(self, learning_goal_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT kw.name "
                "FROM keywords kw "
                "JOIN learningGoal_keywords AS LG_KW ON LG_KW.keyword_id = kw.id "
                "WHERE LG_KW.learningGoal_id = ? ",
                (learning_goal_id,)
            )

            all_results = cur.fetchall()
            return all_results
    def get_studentGroup_average_all_subjects(self, student_group_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(""" WITH latest_snapshots AS (
                    SELECT
                        t.student_id,
                        s.learningGoal_id,
                        MAX(s.at) AS latest_at
                    FROM taxonomies t
                    JOIN snapshots s ON t.snapshot_id = s.id
                    JOIN students st ON t.student_id = st.id
                    JOIN student_studentGroups ssg ON st.id = ssg.student_id
                    WHERE ssg.studentGroup_id = ?  -- Replace with your student group ID
                    GROUP BY t.student_id, s.learningGoal_id
                ),
                student_averages AS (
                    SELECT
                        st.id AS student_id,
                        lg.id AS learningGoal_id,
                        (AVG(t.kennen) + AVG(t.kunnen)) / 2.0 AS avg_kennen_kunnen
                    FROM latest_snapshots ls
                    JOIN students st ON ls.student_id = st.id
                    JOIN snapshots s
                        ON s.learningGoal_id = ls.learningGoal_id
                        AND s.at = ls.latest_at
                    JOIN taxonomies t
                        ON t.student_id = st.id AND t.snapshot_id = s.id
                    JOIN learningGoals lg ON s.learningGoal_id = lg.id
                    GROUP BY st.id, lg.id
                )
                SELECT
                    lg.id AS learningGoal_id,
                    lg.title AS learningGoal_title,
                    sub.id AS subject_id,
                    sub.name AS subject_title,
                    AVG(avg_kennen_kunnen) AS group_avg_kennen_kunnen
                FROM student_averages sa
                JOIN learningGoals lg ON sa.learningGoal_id = lg.id
                JOIN subjects sub ON lg.subject_id = sub.id
                GROUP BY lg.id, sub.id
                ORDER BY lg.id;"""        ,
                (student_group_id,)
            )
            all_results = cur.fetchall()
            return all_results

    def get_student_average_all_learningGoals(self, student_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(""" WITH latest_snapshots AS (
                    SELECT
                        t.student_id,
                        s.learningGoal_id,
                        MAX(s.at) AS latest_at
                    FROM taxonomies t
                    JOIN snapshots s ON t.snapshot_id = s.id
                    WHERE t.student_id = ?  -- Replace with the target student ID
                    GROUP BY t.student_id, s.learningGoal_id
                )
                SELECT
                    lg.id AS learningGoal_id,
                    lg.title AS learningGoal_title,
                    sub.id AS subject_id,
                    sub.name AS subject_title,
                    (AVG(t.kennen) + AVG(t.kunnen)) / 2.0 AS avg_kennen_kunnen
                FROM latest_snapshots ls
                JOIN snapshots s
                    ON s.learningGoal_id = ls.learningGoal_id
                    AND s.at = ls.latest_at
                JOIN taxonomies t
                    ON t.student_id = ls.student_id AND t.snapshot_id = s.id
                JOIN learningGoals lg ON s.learningGoal_id = lg.id
                JOIN subjects sub ON lg.subject_id = sub.id
                GROUP BY lg.id, sub.id
                ORDER BY lg.id;""",
                        (student_id,)
                        )

            all_results = cur.fetchall()
            return all_results

    def get_last_snapshot_of_student(self, student_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(""" SELECT
                        t.id,
                        t.level,
                        t.kennen,
                        t.kunnen,
                        t.confidence,
                        t.student_id,
                        t.snapshot_id,
                        lg.title,
                        s.at
                    FROM taxonomies t
                    INNER JOIN main.snapshots s on s.id = t.snapshot_id
                    INNER JOIN LearningGoals lg ON s.learningGoal_id = lg.id
                    WHERE t.student_id = ?
                        AND t.snapshot_id = (
                            SELECT s2.id
                            FROM snapshots s2
                            JOIN taxonomies t2 ON t2.snapshot_id = s2.id
                            WHERE t2.student_id = t.student_id
                              AND s2.at = (
                                  SELECT MAX(s3.at)
                                  FROM snapshots s3
                                  JOIN taxonomies t3 ON t3.snapshot_id = s3.id
                                  WHERE t3.student_id = t.student_id
                              )
                            LIMIT 1
                        )
                    """,
                        (student_id,)
                        )

            all_results = cur.fetchall()
            return all_results