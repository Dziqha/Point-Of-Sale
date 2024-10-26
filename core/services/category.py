from datetime import datetime
from typing import Optional, Dict, Any, Union
from .base_model import BaseModel
from core.lib import db

class Category(BaseModel):
    def __init__(self, name: str, description: str = ""):
        self.category_id: Optional[int] = None
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    def create(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute(
            '''INSERT INTO categories (name, description, created_at) VALUES (?, ?, ?)''', 
            (self.name, self.description, self.created_at)
        )
        conn.commit()
        success = cursor.rowcount > 0
        category_id = cursor.lastrowid if success else None
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Category '{self.name}' saved successfully." if success else f"Failed to save category '{self.name}'."
        }
        if success:
            response["data"] = {"category_id": category_id}
        
        return response

    def get_all(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM categories''')
        categories = cursor.fetchall()
        conn.close()

        response = {
            "status": "success",
            "message": "Categories retrieved successfully." if categories else "No categories found."
        }
        if categories:
            response["data"] = categories
        
        return response

    def get_by_id(self, category_id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM categories WHERE category_id = ?''', (category_id,))
        category = cursor.fetchone()
        conn.close()

        response = {
            "status": "success" if category else "error",
            "message": "Category retrieved successfully." if category else f"Category with ID {category_id} not found."
        }
        if category:
            response["data"] = category
        
        return response

    def update(self) -> Dict[str, Union[str, Any]]:
        if self.category_id is None:
            return {
                "status": "error",
                "message": "Category ID is required to update a category."
            }

        conn, cursor = db.init_db()
        cursor.execute(
            '''UPDATE categories SET name = ?, description = ? WHERE category_id = ?''', 
            (self.name, self.description, self.category_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Category '{self.name}' updated successfully." if success else f"Failed to update category '{self.name}' or no changes were made."
        }
        
        return response

    def delete(self) -> Dict[str, Union[str, Any]]:
        if self.category_id is None:
            return {
                "status": "error",
                "message": "Category ID is required to delete a category."
            }

        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM categories WHERE category_id = ?''', (self.category_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Category with ID '{self.category_id}' deleted successfully." if success else f"Failed to delete category ith ID '{self.category_id}' or category does not exist."
        }
        
        return response
