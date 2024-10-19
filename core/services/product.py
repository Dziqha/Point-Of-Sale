from datetime import datetime
from typing import Optional
from .base_model import BaseModel
from core.lib import db

class Product(BaseModel):
    def __init__(self, name: str, sku: str, barcode: str, category_id: int, price: int, description: str = ""):
        self.product_id: Optional[int] = None
        self.name = name
        self.sku = sku
        self.barcode = barcode
        self.category_id = category_id
        self.stock = 0
        self.price = price
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        cursor.execute('''INSERT INTO products (name, sku, barcode, category_id, stock, price, description, created_at, updated_at) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (self.name, self.sku, self.barcode, self.category_id, self.stock, self.price, self.description, self.created_at, self.updated_at))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return f"Product '{self.name}' created successfully."
        else:
            return f"Failed to create product '{self.name}'."

    def get_all(self):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM products''')
        products = cursor.fetchall()
        conn.close()
        return products

    def get_by_id(self, product_id: int):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM products WHERE product_id = ?''', (product_id,))
        product = cursor.fetchone()
        conn.close()
        return product

    def update(self) -> str:
        if self.product_id is None:
            raise ValueError("Product ID is required to update a product.")

        self.updated_at = datetime.now()

        conn, cursor = db.init_db()
        cursor.execute('''UPDATE products SET name = ?, sku = ?, barcode = ?, category_id = ?, stock = ?, price = ?, description = ?, updated_at = ? 
                          WHERE product_id = ?''', 
                       (self.name, self.sku, self.barcode, self.category_id, self.stock, self.price, self.description, self.updated_at, self.product_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return f"Product '{self.name}' updated successfully."
        else:
            return f"Failed to update product '{self.name}' or no changes were made."

    def delete(self) -> str:
        if self.product_id is None:
            raise ValueError("Product ID is required to delete a product.")

        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM products WHERE product_id = ?''', (self.product_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return f"Product '{self.name}' deleted successfully."
        else:
            return f"Failed to delete product '{self.name}' or product does not exist."

    def search_by_name(self, name: str):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM products WHERE name LIKE ?''', (f'%{name}%',))
        products = cursor.fetchall()
        conn.close()
        return products

    def search_by_barcode(self, barcode: str):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM products WHERE barcode = ?''', (barcode,))
        product = cursor.fetchone()
        conn.close()
        return product
