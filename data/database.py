import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
        self._setup_tables()

    def connect(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys = ON')
        return con

    def _setup_tables(self):
        with self.connect() as con:
            cur = con.cursor()

            # Roles
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS roles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )
                ''')

            # USERS
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT,
                    password TEXT NOT NULL,
                    role_id INTEGER,
                    FOREIGN KEY (role_id) REFERENCES role(id)
                )
            ''')

            # Teachers
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS teachers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL UNIQUE,
                        first_name TEXT,
                        last_name TEXT,
                        postcode TEXT,
                        gender TEXT,
                        city TEXT,
                        country TEXT,
                        street_name TEXT,
                        birth_date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                ''')

            # Students
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    first_name TEXT,
                    last_name TEXT,
                    postcode TEXT,
                    gender TEXT,
                    city TEXT,
                    country TEXT,
                    street_name TEXT,
                    birth_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

            # StudentGroup
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS studentGroups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )
                ''')

            # students ↔ studentGroup
            cur.execute('''
                CREATE TABLE IF NOT EXISTS student_studentGroups (
                    student_id INTEGER NOT NULL,
                    studentGroup_id INTEGER NOT NULL,
                    PRIMARY KEY (student_id, studentGroup_id),
                    FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY(studentGroup_id) REFERENCES studentGroups(id) ON DELETE CASCADE
                )
            ''')

            # subject
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS subjects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )
                ''')

            # subjects ↔ studentGroup
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS studentGroup_subjects (
                        subject_id INTEGER NOT NULL,
                        studentGroup_id INTEGER NOT NULL,
                        PRIMARY KEY (subject_id, studentGroup_id),
                        FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
                        FOREIGN KEY(studentGroup_id) REFERENCES studentGroups(id) ON DELETE CASCADE
                    )
                ''')

            # LearningGoals
            cur.execute('''
                   CREATE TABLE IF NOT EXISTS learningGoals (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       subject_id INTEGER NOT NULL,
                       FOREIGN KEY(subject_id) REFERENCES subjects(id)
                   )
               ''')

            # learnGoal_keywords
            cur.execute('''
                   CREATE TABLE IF NOT EXISTS learnGoal_keywords (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       learningGoal_id INTEGER NOT NULL,
                       FOREIGN KEY(learningGoal_id) REFERENCES learningGoals(id)
                   )
               ''')

            # sources
            cur.execute('''
                   CREATE TABLE IF NOT EXISTS sources (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       source_id TEXT NOT NULL UNIQUE,
                       type TEXT NOT NULL
                   )
               ''')

            # snapshots
            cur.execute('''
                  CREATE TABLE IF NOT EXISTS snapshots (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      at DATE NOT NULL,
                      learningGoal_id INTEGER NOT NULL,
                      source_id INTEGER NOT NULL,
                      FOREIGN KEY(learningGoal_id) REFERENCES learningGoals(id),
                      FOREIGN KEY(source_id) REFERENCES source(id)

                  )
              ''')
            # taxonomy

            cur.execute('''
                      CREATE TABLE IF NOT EXISTS taxonomy (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          kennen INTERGER,
                          kunnen INTEGER,
                          confidence INTEGER,
                          snapshot_id INTEGER NOT NULL,
                          student_id INTEGER NOT NULL,
                          FOREIGN KEY(snapshot_id) REFERENCES snapshots(id),
                          FOREIGN KEY(student_id) REFERENCES students(id)

                      )
                  ''')

            con.commit()
