from .user import User
from typing import Dict, Union, Any
from core.lib import db

class Cashier(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, role='cashier')
    
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
                "message": f"Cashier '{self.username}' created successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to create cashier '{self.username}'."
            }
    
    def get_all(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''
            SELECT * FROM users WHERE role = 'cashier'
        ''')
        users = cursor.fetchall()
        conn.close()

        if users:
            return {
                "status": "success",
                "message": "Cashier retrieved successfully.",
                "data": users
            }
        else:
            return {
                "status": "info",
                "message": "No cashier found.",
                "data": []
            }
    
    def get_by_id(self, user_id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM users WHERE user_id = ? AND role = "cashier"''', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {
                "status": "success",
                "message": "Cashier retrieved successfully.",
                "data": user
            }
        else:
            return {
                "status": "error",
                "message": f"Cashier with ID {user_id} not found."
            }
    
    def update(self) -> Dict[str, Union[str, Any]]:
        if self.user_id is None:
            return {
                "status": "error",
                "message": "Cashier ID is required to update a cashier."
            }

        conn, cursor = db.init_db()
        cursor.execute('''UPDATE users SET username = ?, password = ? 
                          WHERE user_id = ?''', 
                       (self.username, self.password, self.user_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return {
                "status": "success",
                "message": f"Cashier '{self.username}' updated successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to update cashier '{self.username}' or no changes were made."
            }
    
    def delete(self) -> Dict[str, Union[str, Any]]:
        if self.user_id is None:
            return {
                "status": "error",
                "message": "Cashier ID is required to delete a cashier."
            }

        conn, cursor = db.init_db()
        cursor.execute('''
        DELETE FROM users 
        WHERE user_id = ? AND role = 'cashier'
        ''', (self.user_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return {
                "status": "success",
                "message": f"Cashier with ID '{self.user_id}' deleted successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to delete cashier with ID '{self.user_id}' or cashier does not exist."
            }