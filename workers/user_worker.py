from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

class UserWorker:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_user(self, user_name, password):
        hashed_password = pwd_context.hash(password)
        self.cursor.execute(
            "INSERT INTO users (user_name, password_hash) VALUES (%s, %s) RETURNING user_id",
            (user_name, hashed_password)
        )
        user_id = self.cursor.fetchone()[0]
        return user_id

    def verify_user(self, user_name, password):
        self.cursor.execute(
            "SELECT user_id, password_hash FROM users WHERE user_name = %s",
            (user_name,)
        )
        result = self.cursor.fetchone()
        if result is None:
            return None
        ps_result = pwd_context.verify(password, result[1])
        if not ps_result:
            return None
        return result[0]