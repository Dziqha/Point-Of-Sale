from datetime import datetime
from typing import Optional
from .base_model import BaseModel
from core.lib import db

class Category(BaseModel):
    def __init__(self, name: str, description: str = ""):
        self.category_id: Optional[int] = None
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        cursor.execute('''INSERT INTO categories (name, description, created_at) VALUES (?, ?, ?)''', 
                       (self.name, self.description, self.created_at))
        conn.commit()
        conn.close()
        
        if cursor.rowcount > 0:
            return f"Category '{self.name}' saved successfully."
        else:
            return f"Failed to save category '{self.name}'."

    def get_all(self):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM categories''')
        categories = cursor.fetchall()
        conn.close()
        return categories

    def get_by_id(self, category_id: int):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM categories WHERE category_id = ?''', (category_id,))
        category = cursor.fetchone()
        conn.close()
        return category

    def update(self) -> str:
        if self.category_id is None:
            raise ValueError("Category ID is required to update a category.")

        conn, cursor = db.init_db()
        cursor.execute('''UPDATE categories SET name = ?, description = ? WHERE category_id = ?''', 
                       (self.name, self.description, self.category_id))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return f"Category '{self.name}' updated successfully."
        else:
            return f"Failed to update category '{self.name}' or no changes were made."

    def delete(self) -> str:
        if self.category_id is None:
            raise ValueError("Category ID is required to delete a category.")

        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM categories WHERE category_id = ?''', (self.category_id,))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return f"Category '{self.name}' deleted successfully."
        else:
            return f"Failed to delete category '{self.name}' or category does not exist."