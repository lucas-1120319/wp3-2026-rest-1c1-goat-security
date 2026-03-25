import sqlite3
from data.database import Database
from models.user import User

class Teacher:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def get_all_user_info(self, user_id: int):
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <--- make rows dictionary-like
            cur = con.cursor()
            cur.execute("""SELECT user_id, email, phone, first_name, last_name, birth_date 
                           FROM teachers
                        inner join users ON teachers.user_id = users.id WHERE user_id = ?
                        """, (user_id,))
            return cur.fetchone()

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
                               birth_date  = ?
                           WHERE user_id = ?""",
                        (data["first_name"], data["last_name"], data["birth_date"], user_id,))
            con.commit()

            if data.get("password"):
                cur.execute("""
                            UPDATE users
                            SET email    = ?,
                                phone    = ?,
                                password = ?
                            WHERE id = ?
                            """,                         (data["email"], data["phone"], User.hash_password(data["password"]), user_id,))

            else:
                cur.execute("""
                            UPDATE users
                            SET email = ?,
                                phone = ?
                            WHERE id = ?
                            """, (data["email"], data["phone"], user_id))

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

    def get_group_per_name(self, get_group_per_name: str):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT studentGroups.id FROM teacher_studentGroup "
                        "INNER JOIN studentGroups ON studentGroups.id = teacher_studentGroup.studentGroup_id "
                        "WHERE studentGroups.name = ? ",
                        (get_group_per_name,))
            con.commit()
            return cur.fetchone()[0]

    def get_all_studentGroups(self):
        """ Get all studentGroups """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT studentGroups.name, studentGroups.id FROM studentGroups",)
            con.commit()
            return cur.fetchall()

    def format_class_data(self, rows):
        result = {
            "class": None,
            "students": []
        }

        students_map = {}

        for row in rows:
            (
                class_id, class_name,
                student_id, first_name, last_name, birth_date,
                lg_id, lg_title, subject_title, avg_score
            ) = row

            # Set class info once
            if result["class"] is None:
                result["class"] = {
                    "id": class_id,
                    "name": class_name
                }

            # Create student if not exists
            if student_id not in students_map:
                students_map[student_id] = {
                    "id": student_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "birth_date": birth_date,
                    "subjects": {}  # 👈 use dict first (important!)
                }

            student = students_map[student_id]

            # Create subject if not exists
            if subject_title not in student["subjects"]:
                student["subjects"][subject_title] = {
                    "name": subject_title,
                    "learning_goals": []
                }

            # Add learning goal to correct subject
            student["subjects"][subject_title]["learning_goals"].append({
                "id": lg_id,
                "title": lg_title,
                "avg": avg_score
            })

        # Convert subjects dict → list
        for student in students_map.values():
            student["subjects"] = list(student["subjects"].values())

        result["students"] = list(students_map.values())
        return result

    def get_all_students_studentGroup(self, class_id: int):
        """ Get all students from a studentGroup """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                WITH class_info AS (
                    SELECT id, name
                    FROM studentGroups
                    WHERE id = ?
                ),
                class_students AS (
                    SELECT
                        s.id AS student_id,
                        s.first_name,
                        s.last_name,
                        s.birth_date,
                        sg.id AS class_id,
                        sg.name AS class_name
                    FROM students s
                    JOIN student_studentGroups ssg ON s.id = ssg.student_id
                    JOIN studentGroups sg ON sg.id = ssg.studentGroup_id
                    WHERE sg.id = ?
                ),
                latest_snapshots AS (
                    SELECT
                        t.student_id,
                        s.learningGoal_id,
                        MAX(s.at) AS latest_at
                    FROM taxonomies t
                    JOIN snapshots s ON t.snapshot_id = s.id
                    WHERE t.student_id IN (SELECT student_id FROM class_students)
                    GROUP BY t.student_id, s.learningGoal_id
                )
                SELECT
                    cs.class_id,
                    cs.class_name,
                    cs.student_id,
                    cs.first_name,
                    cs.last_name,
                    cs.birth_date,
                    lg.id AS learningGoal_id,
                    lg.title AS learningGoal_title,
                    sub.name AS subject_title,
                    (AVG(t.kennen) + AVG(t.kunnen)) / 2.0 AS avg_score
                FROM latest_snapshots ls
                JOIN class_students cs ON cs.student_id = ls.student_id
                JOIN snapshots s
                    ON s.learningGoal_id = ls.learningGoal_id
                    AND s.at = ls.latest_at
                JOIN taxonomies t
                    ON t.student_id = ls.student_id AND t.snapshot_id = s.id
                JOIN learningGoals lg ON lg.id = s.learningGoal_id
                JOIN subjects sub ON sub.id = lg.subject_id
                GROUP BY
                    cs.student_id,
                    lg.id
                ORDER BY cs.student_id, lg.id;
            """,
                (class_id,class_id,))
            rows = cur.fetchall()
            data = self.format_class_data(rows)
            return data



    def get_single_student_subject(self, student_id: int):
        """ Get the average result of a student from a subject """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT 
                    subjects.id,
                    subjects.name,
                    ROUND((AVG(taxonomies.kennen) + AVG(taxonomies.kunnen)) / 2.0, 2) AS average,
                    ROUND(AVG(taxonomies.confidence), 2) AS confidence
                FROM taxonomies JOIN snapshots ON snapshots.id = taxonomies.snapshot_id
                JOIN learningGoals ON learningGoals.id = snapshots.learningGoal_id
                JOIN subjects ON subjects.id = learningGoals.subject_id
                WHERE taxonomies.student_id = ?
                GROUP BY subjects.id
                """,
                (student_id,)
            )

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

    def get_learning_goal_by_class(self, class_id, subject_id):
        """ Get list of a group with selected learning goal. """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT
                        sg.name AS class_name,
                        sg.id AS class_id,
                        st.first_name AS student_name,
                        lg.id AS learning_goal_id,
                        lg.title AS learning_goal,
                        tax.level AS level,
                        AVG(tax.kennen + tax.kunnen) / 2 AS average
                    FROM taxonomies tax
                    JOIN students st ON st.id = tax.student_id
                    JOIN snapshots ss ON ss.id = tax.snapshot_id
                    JOIN learningGoals lg ON lg.id = ss.learningGoal_id
                    JOIN student_studentGroups ssg ON ssg.student_id = st.id
                    JOIN studentGroups sg ON sg.id = ssg.studentGroup_id
                    
                    WHERE sg.id = ? AND lg.subject_id = ?
                    
                    GROUP BY st.id, lg.id
                    ORDER BY lg.id, st.first_name
                    
                """,
                (class_id, subject_id)
            )
            result = cur.fetchall()
            return result





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