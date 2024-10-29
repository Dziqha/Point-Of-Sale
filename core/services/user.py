import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Union, Any
from .base_model import BaseModel
from .person import Person
from core.lib import db
from core.lib.hash import verify_password
from core.middlewares.auth import SECRET_KEY

class User(Person, BaseModel):
    def __init__(self, username: str, password: str, role: str):
        super().__init__(name=username)
        self.user_id: Optional[int] = None
        self.username = username
        self.password = password
        self.role = role

    def create(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''INSERT INTO users (username, password, role, created_at) 
                          VALUES (?, ?, ?, ?)''', 
                       (self.username, self.password, self.role, self.created_at))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return {
                "status": "success",
                "message": f"User  '{self.username}' created successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to create user '{self.username}'."
            }

    def get_all(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''
            SELECT * FROM users WHERE role != 'superuser'
        ''')
        users = cursor.fetchall()
        conn.close()

        if users:
            return {
                "status": "success",
                "message": "Users retrieved successfully.",
                "data": users
            }
        else:
            return {
                "status": "info",
                "message": "No users found.",
                "data": []
            }

    def get_by_id(self, user_id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {
                "status": "success",
                "message": "User  retrieved successfully.",
                "data": user
            }
        else:
            return {
                "status": "error",
                "message": f"User  with ID {user_id} not found."
            }

    def get_by_role(self, role: str) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users WHERE role = ?''', (role,))
        users = cursor.fetchall()
        conn.close()

        if users:
            return {
                "status": "success",
                "message": "Users retrieved successfully.",
                "data": users
            }
        else:
            return {
                "status": "info",
                "message": f"No users found with role '{role}'.",
                "data": []
            }

    def update(self) -> Dict[str, Union[str, Any]]:
        if self.user_id is None:
            return {
                "status": "error",
                "message": "User  ID is required to update a user."
            }

        conn, cursor = db.init_db()
        cursor.execute('''UPDATE users SET username = ?, password = ?, role = ? 
                          WHERE user_id = ?''', 
                       (self.username, self.password, self.role, self.user_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return {
                "status": "success",
                "message": f"User  '{self.username}' updated successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to update user '{self.username}' or no changes were made."
            }

    def delete(self) -> Dict[str, Union[str, Any]]:
        if self.user_id is None:
            return {
                "status": "error",
                "message": "User  ID is required to delete a user."
            }

        conn, cursor = db.init_db()
        cursor.execute('''
        DELETE FROM users 
        WHERE user_id = ? AND role != 'superuser'
        ''', (self.user_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return {
                "status": "success",
                "message": f"User with ID '{self.user_id}' deleted successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to delete user with ID '{self.user_id}' or user does not exist."
            }

    def login(self, username: str, password: str) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and verify_password(user[2], password):
            self.user_id = user[0]
            self.username = user [1]
            self.password = user[2]
            self.role = user[3]

            session_data = {
                'user_id': self.user_id,
                'username': self.username,
                'role': self.role,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(session_data, SECRET_KEY, algorithm="HS256")

            return {
                "status": "success",
                "message": "Login successful.",
                "token": token
            }
        else:
            return {
                "status": "error",
                "message": "Invalid username or password."
            }

    def get_current_session(self, token: str) -> Dict[str, Union[str, Any]]:
        try:
            session_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return {
                "status": "success",
                "message": "Session retrieved successfully.",
                "data": session_data
            }
        except jwt.ExpiredSignatureError:
            return {
                "status": "error",
                "message": "Session expired. Please log in again."
            }
        except jwt.InvalidTokenError:
            return {
                "status": "error",
                "message": "Invalid session token."
            }