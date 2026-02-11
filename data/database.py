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
                    FOREIGN KEY (role_id) REFERENCES roles(id)
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
                    external_id INTEGER UNIQUE,
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
                        name TEXT NOT NULL UNIQUE,
                        external_id INTEGER UNIQUE
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
                       external_id TEXT UNIQUE,
                       title TEXT NOT NULL,
                       subject_id INTEGER NOT NULL,
                       FOREIGN KEY(subject_id) REFERENCES subjects(id)
                   )
               ''')

            # keywords
            cur.execute('''
                   CREATE TABLE IF NOT EXISTS keywords (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE
                   )
               ''')

            # learningGoals ↔ keywords
            cur.execute('''
                   CREATE TABLE IF NOT EXISTS learningGoal_keywords (
                       learningGoal_id INTEGER NOT NULL,
                       keyword_id INTEGER NOT NULL,
                    UNIQUE(learningGoal_id, keyword_id),
                       FOREIGN KEY(learningGoal_id) REFERENCES learningGoals(id) ON DELETE CASCADE,
                       FOREIGN KEY(keyword_id) REFERENCES keywords(id) ON DELETE CASCADE
                   )
               ''')

            # sources
            cur.execute('''
                   CREATE TABLE IF NOT EXISTS sources (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       external_id TEXT UNIQUE,
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
                          UNIQUE(learningGoal_id, source_id, at),

                      FOREIGN KEY(learningGoal_id) REFERENCES learningGoals(id),
                      FOREIGN KEY(source_id) REFERENCES sources(id)

                  )
              ''')
            # taxonomy

            cur.execute('''
                  CREATE TABLE IF NOT EXISTS taxonomies (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      level TEXT NOT NULL,
                      kennen NUMERIC(3,2) NOT NULL,
                      kunnen NUMERIC(3,2) NOT NULL,
                      confidence NUMERIC(3,2) NOT NULL,
                      snapshot_id INTEGER NOT NULL,
                      student_id INTEGER NOT NULL,
                      FOREIGN KEY(snapshot_id) REFERENCES snapshots(id),
                      FOREIGN KEY(student_id) REFERENCES students(id)

                  )
              ''')

            cur.execute('''
                        CREATE TABLE IF NOT EXISTS teacher_studentGroup
                        (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            studentGroup_id  INTEGER   NOT NULL,
                            teacher_id  INTEGER   NOT NULL,
                          UNIQUE(studentGroup_id, teacher_id),

                            FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                            FOREIGN KEY (studentGroup_id) REFERENCES studentGroups (id)
                        )
                        ''')

            roles = ["admin", "student", "teacher"]
            for role in roles:
                cur.execute(
                    "INSERT OR IGNORE INTO roles (name) VALUES (?)",
                    (role,)
                )

            con.commit()
