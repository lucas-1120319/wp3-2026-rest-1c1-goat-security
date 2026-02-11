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
        json_path = self.json_path
        with self.db.connect() as con:
            cur = con.cursor()

        if not os.path.exists(self.json_path):
            print(f"File '{self.json_path}' does not exist.")
            return  # stop the function safely

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        #go record for record
        for entry in data["entries"]:
            #grab the students info and create some default info for the users table
            student = entry["student"]
            email = f"{student['name'].lower()}@example.com"
            password = "geheim"

            role_id =  2 # student in database

            # Insert into users
            cur.execute(
                "INSERT OR IGNORE INTO users (email, password, role_id ) VALUES (?, ? , ? )",
                (email, password, role_id,)
            )
            #grab the last added id and insert the that we got about the student
            user_id = cur.lastrowid  # get the PK
            cur.execute("INSERT OR IGNORE INTO students (user_id, external_id, first_name) VALUES (?,?, ?)", (user_id, student["id"], student["name"],))
            cur.execute(
                "SELECT id FROM students WHERE external_id = ?",
                (student["id"],)
            )
            student_id = cur.fetchone()[0]

            #get the subject and add if it doesnt exist yet
            subject = entry["subject"]
            cur.execute("INSERT OR IGNORE INTO subjects (external_id, name) VALUES (?, ?)", (subject["id"], subject["name"],))
            #fetch the last id for the subject
            cur.execute(
                "SELECT id FROM subjects WHERE external_id = ?",
                (subject["id"],)
            )
            subject_id = cur.fetchone()[0]

            #get the learngoal and add it to the db with link to the subject
            learningGoals = entry["learningGoals"]
            for learningGoal in learningGoals:
                #insert all learning goals per subject and get the learing goal with same id
                cur.execute("INSERT OR IGNORE INTO learningGoals (external_id ,title, subject_id) VALUES (?, ?, ?)",(learningGoal["id"],learningGoal["title"], subject_id,))
                cur.execute(
                    "SELECT id FROM learningGoals WHERE external_id = ?",
                    (learningGoal["id"],)
                )
                learningGoal_id = cur.fetchone()[0]


                keywords = learningGoal["keywords"]
                for keyword in keywords:
                    #insert all the unique keywords
                    cur.execute("INSERT OR IGNORE INTO keywords (name) VALUES ( ?)",(keyword,))

                    cur.execute(
                        "SELECT id FROM keywords WHERE name = ?",
                        (keyword,)
                    )
                    keyword_id = cur.fetchone()[0]
                    #link the keywords together
                    cur.execute("INSERT OR IGNORE INTO learningGoal_keywords (learningGoal_id, keyword_id) VALUES ( ?, ?)",(learningGoal_id,keyword_id,))

                snapshots = learningGoal["snapshots"]
                for snapshot in snapshots:
                    #add the source of its unique
                    source = snapshot["source"]
                    cur.execute("INSERT OR IGNORE INTO sources (external_id, type) VALUES ( ?, ?)",(source["id"], source["type"],))
                    cur.execute(
                        "SELECT id FROM sources WHERE external_id = ?",
                        (source["id"],)
                    )
                    source_id = cur.fetchone()[0]

                    cur.execute("INSERT OR IGNORE INTO snapshots (at, learningGoal_id, source_id) VALUES ( ?, ?,? )",(snapshot["at"], learningGoal_id,source_id,))
                    cur.execute(
                        "SELECT id FROM snapshots WHERE source_id = ? and learningGoal_id = ? and at = ?",
                        (source_id, learningGoal_id,snapshot["at"],)
                    )
                    snapshot_id = cur.fetchone()[0]
                    taxonomies = snapshot["taxonomy"]
                    for taxonomy in taxonomies:
                        cur.execute(
                            "INSERT OR IGNORE INTO taxonomies (level,kennen, kunnen, confidence, snapshot_id, student_id) VALUES ( ?, ?,?, ? ,?, ? )",
                            (taxonomy["level"], taxonomy["kennen"],taxonomy["kunnen"], taxonomy["confidence"], snapshot_id, student_id,))

        con.commit()