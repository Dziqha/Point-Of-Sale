from datetime import datetime
from typing import Optional
from .base_model import BaseModel
from lib import db

class User(BaseModel):
    def __init__(self, username: str, password: str, role: str):
        self.user_id: Optional[int] = None
        self.username = username
        self.password = password
        self.role = role
        self.created_at = datetime.now()

    def save(self):
        # Implementation to save user to database
        conn, cursor = db.init_db()
        cursor.execute('''INSERT INTO users (username, password, role) VALUES (?, ?, ?)''', (self.username, self.password, self.role),)
        conn.commit()
        conn.close()
        print(f"User {self.username} saved to database.")

    def delete(self):
        # Implementation to delete user from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve user by ID
        pass
