import sqlite3
from data.database import Database


class User:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def authenticate(self, email, password):
        """validate user's email and password"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM users WHERE email = ? and password = ?",
                (email, password),
            )
            con.commit()
            return cur.fetchone()

    def get_user_role(self, user_id):
        """ get the current user's role """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM users LEFT JOIN roles ON users.role_id = roles.id WHERE users.id = ?",
                (user_id,),
            )
            con.commit()
            return cur.fetchone()

    def get_current_user(self, user_id):
        """Getting the current user"""
        if not user_id:
            return None

        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            con.commit()
            return cur.fetchone()