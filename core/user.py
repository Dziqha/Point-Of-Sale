from datetime import datetime
from typing import Optional
from .base_model import BaseModel
from .lib import db

class User(BaseModel):
    def __init__(self, username: str, password: str, role: str):
        self.user_id: Optional[int] = None
        self.username = username
        self.password = password
        self.role = role
        self.created_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        cursor.execute('''INSERT INTO users (username, password, raole, created_at) 
                          VALUES (?, ?, ?, ?)''', 
                       (self.username, self.password, self.role, self.created_at))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return f"User '{self.username}' created successfully."
        else:
            return f"Failed to create user '{self.username}'."

    def get_all(self):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users''')
        users = cursor.fetchall()
        conn.close()
        return users

    def get_by_id(self, user_id: int):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def update(self) -> str:
        if self.user_id is None:
            raise ValueError("User ID is required to update a user.")

        conn, cursor = db.init_db()
        cursor.execute('''UPDATE users SET username = ?, password = ?, role = ? 
                          WHERE user_id = ?''', 
                       (self.username, self.password, self.role, self.user_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return f"User '{self.username}' updated successfully."
        else:
            return f"Failed to update user '{self.username}' or no changes were made."

    def delete(self) -> str:
        if self.user_id is None:
            raise ValueError("User ID is required to delete a user.")

        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM users WHERE user_id = ?''', (self.user_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return f"User '{self.username}' deleted successfully."
        else:
            return f"Failed to delete user '{self.username}' or user does not exist."

    def login(self, username: str, password: str):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.user_id = user[0]
            self.username = user[1]
            self.password = user[2]
            self.role = user[3]
        return self

    def logout(self) -> str:
        self.user_id = None
        self.username = None
        self.role = None
        return "User logged out successfully."
