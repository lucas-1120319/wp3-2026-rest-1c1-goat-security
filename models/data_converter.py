import sqlite3
from data.database import Database
import json
import os

class data_converter:
    def __init__(self, db_path: str, json_path: str):
        self.db = Database(db_path)
        self.json_path = json_path
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.json_path):
            print(f"File '{self.json_path}' does not exist.")
            return

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        with self.db.connect() as con:
            cur = con.cursor()

            for student_entry in data["students"]:
                student = student_entry["student"]
                email = f"{student['name'].lower()}@example.com"
                password = "geheim"
                role_id = 2  # student

                # Insert user
                cur.execute(
                    "INSERT OR IGNORE INTO users (email, password, role_id) VALUES (?, ?, ?)",
                    (email, password, role_id)
                )
                user_id = cur.lastrowid
                cur.execute(
                    "INSERT OR IGNORE INTO students (user_id, external_id, first_name) VALUES (?, ?, ?)",
                    (user_id, student["id"], student["name"])
                )

                # Get student_id
                cur.execute(
                    "SELECT id FROM students WHERE external_id = ?",
                    (student["id"],)
                )
                student_id = cur.fetchone()[0]

                # Loop over subjects
                for subj_entry in student_entry["subjects"]:
                    subject = subj_entry["subject"]

                    # Insert subject if not exists
                    cur.execute(
                        "INSERT OR IGNORE INTO subjects (external_id, name) VALUES (?, ?)",
                        (subject["id"], subject["name"])
                    )
                    cur.execute(
                        "SELECT id FROM subjects WHERE external_id = ?",
                        (subject["id"],)
                    )
                    subject_id = cur.fetchone()[0]

                    # Loop over learning goals
                    for lg in subj_entry["learningGoals"]:
                        # Insert learning goal linked to subject
                        cur.execute(
                            "INSERT OR IGNORE INTO learningGoals (external_id, title, subject_id) VALUES (?, ?, ?)",
                            (lg["id"], lg["title"], subject_id)
                        )
                        cur.execute(
                            "SELECT id FROM learningGoals WHERE external_id = ?",
                            (lg["id"],)
                        )
                        learningGoal_id = cur.fetchone()[0]

                        # Insert keywords and link them
                        for keyword in lg["keywords"]:
                            cur.execute(
                                "INSERT OR IGNORE INTO keywords (name) VALUES (?)",
                                (keyword,)
                            )
                            cur.execute(
                                "SELECT id FROM keywords WHERE name = ?",
                                (keyword,)
                            )
                            keyword_id = cur.fetchone()[0]
                            cur.execute(
                                "INSERT OR IGNORE INTO learningGoal_keywords (learningGoal_id, keyword_id) VALUES (?, ?)",
                                (learningGoal_id, keyword_id)
                            )

                        # Loop over snapshots
                        for snapshot in lg.get("snapshots", []):
                            source = snapshot["source"]

                            # Insert source
                            cur.execute(
                                "INSERT OR IGNORE INTO sources (external_id, type) VALUES (?, ?)",
                                (source["id"], source["type"])
                            )
                            cur.execute(
                                "SELECT id FROM sources WHERE external_id = ?",
                                (source["id"],)
                            )
                            source_id = cur.fetchone()[0]

                            # Insert snapshot linked to learningGoal_id
                            cur.execute(
                                "INSERT OR IGNORE INTO snapshots (at, source_id, learningGoal_id) VALUES (?, ?, ?)",
                                (snapshot["at"], source_id, learningGoal_id)
                            )

                            cur.execute(
                                "SELECT id FROM snapshots WHERE source_id=? AND learningGoal_id=? AND at=?",
                                (source_id, learningGoal_id, snapshot["at"])
                            )
                            row = cur.fetchone()
                            if row:
                                snapshot_id = row[0]
                            else:
                                # if somehow not exists, insert explicitly
                                cur.execute(
                                    "INSERT INTO snapshots (at, source_id, learningGoal_id) VALUES (?, ?, ?)",
                                    (snapshot["at"], source_id, learningGoal_id)
                                )
                                snapshot_id = cur.lastrowid

                            # Insert taxonomies
                            for taxonomy in snapshot.get("taxonomy", []):
                                cur.execute(
                                    "INSERT OR IGNORE INTO taxonomies "
                                    "(level, kennen, kunnen, confidence, snapshot_id, student_id) "
                                    "VALUES (?, ?, ?, ?, ?, ?)",
                                    (
                                        taxonomy["level"],
                                        taxonomy["kennen"],
                                        taxonomy["kunnen"],
                                        taxonomy["confidence"],
                                        snapshot_id,
                                        student_id
                                    )
                                )

            con.commit()