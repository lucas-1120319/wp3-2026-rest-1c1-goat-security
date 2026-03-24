import os
import binascii
import hashlib
from data.database import Database


class User:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    @staticmethod
    def hash_password(password):
        """ Used to hash a password """
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )
        return f"{binascii.hexlify(salt).decode()}${binascii.hexlify(hashed).decode()}"

    @staticmethod
    def verify_password(db_password, check_password):
        """ verify a hashed password with a normal password """
        salt_hex, hash_hex = db_password.split("$")
        salt = binascii.unhexlify(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            check_password.encode("utf-8"),
            salt,
            100000
        )

        print(binascii.hexlify(new_hash).decode(), hash_hex)
        return binascii.hexlify(new_hash).decode() == hash_hex

    def authenticate(self, email, password):
        """ validate user's email and password (checking for hashing) """
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            )
            con.commit()
            user = cur.fetchone()

            if not user:
                return None

            stored_password = user["password"]
            if self.verify_password(stored_password, password):
                return user

            return None

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