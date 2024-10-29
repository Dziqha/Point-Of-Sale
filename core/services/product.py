from datetime import datetime
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from core.lib import db

class Product(BaseModel):
    def __init__(self, name: str, sku: str, barcode: str, category_id: int, price: float, description: str = ""):
        self.product_id: Optional[int] = None
        self.name = name
        self.sku = sku
        self.barcode = barcode
        self.category_id = category_id
        self.price = price
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def create(self) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''INSERT INTO products (name, sku, barcode, category_id, price, description, created_at, updated_at) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (self.name, self.sku, self.barcode, self.category_id, self.price, self.description, self.created_at, self.updated_at))
            conn.commit()
            if cursor.rowcount > 0:
                self.product_id = cursor.lastrowid
                return {
                    "status": "success",
                    "message": f"Product {self.name} saved to database.",
                    "data": {"product_id": self.product_id}
                }
            else:
                return {"status": "error", "message": "Failed to save product."}
        except Exception as e:
            return {"status": "error", "message": f"Error creating product: {str(e)}"}
        finally:
            conn.close()

    def update(self) -> dict:
        if self.product_id is None:
            return {"status": "error", "message": "Product ID is not set."}

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            self.updated_at = datetime.now()
            cursor.execute('''UPDATE products 
                          SET name = ?, sku = ?, barcode = ?, category_id = ?, 
                          price = ?, description = ?, updated_at = ? 
                          WHERE product_id = ?''', 
                       (self.name, self.sku, self.barcode, self.category_id, self.price, self.description, 
                        self.updated_at, self.product_id))
            conn.commit()
            if cursor.rowcount > 0:
                return {"status": "success", "message": f"Product with ID {self.product_id} updated in database."}
            else:
                return {"status": "error", "message": "Failed to update product."}
        except Exception as e:
            return {"status": "error", "message": f"Error updating product: {str(e)}"}
        finally:
            conn.close()

    def delete(self) -> dict:
        if self.product_id is None:
            return {"status": "error", "message": "Product ID is not set."}

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''DELETE FROM products WHERE product_id = ?''', (self.product_id,))
            conn.commit()
            if cursor.rowcount > 0:
                return {"status": "success", "message": f"Product with ID {self.product_id} deleted from database."}
            else:
                return {"status": "error", "message": "Failed to delete product."}
        except Exception as e:
            return {"status": "error", "message": f"Error deleting product: {str(e)}"}
        finally:
            conn.close()

    def get_by_id(self, id: int) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.category_id 
                WHERE p.product_id = ?
            ''', (id,))
            product = cursor.fetchone()
            
            if product:
                return {
                    "status": "success",
                    "message": "Product found.",
                    "data": product
                }
            return {"status": "error", "message": "Product not found."}
        except Exception as e:
            return {"status": "error", "message": f"Error retrieving product: {str(e)}"}
        finally:
            conn.close()

    def get_all(self) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.category_id
            ''')
            products = cursor.fetchall()
            return {
                "status": "success",
                "message": "Products retrieved successfully.",
                "data": products
            }
        except Exception as e:
            return {"status": "error", "message": f"Error retrieving products: {str(e)}"}
        finally:
            conn.close()

    def get_out_of_stock(self) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.category_id 
                WHERE p.stock <= 0
            ''')
            products = cursor.fetchall()
            return {
                "status": "success",
                "message": "Out of stock products retrieved successfully.",
                "data": products
            }
        except Exception as e:
            return {"status": "error", "message": f"Error retrieving out of stock products: {str(e)}"}
        finally:
            conn.close()

    def search_by_name(self, name: str) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.category_id 
                WHERE p.name LIKE ?
            ''', (f'%{name}%',))
            products = cursor.fetchall()
            return {
                "status": "success",
                "message": "Products search completed.",
                "data": products
            }
        except Exception as e:
            return {"status": "error", "message": f"Error searching products: {str(e)}"}
        finally:
            conn.close()

    def search_by_barcode(self, barcode: str) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.category_id 
                WHERE p.barcode LIKE ?
            ''', (f'%{barcode}%',))
            products = cursor.fetchall()
            return {
                "status": "success",
                "message": "Products search completed.",
                "data": products
            }
        except Exception as e:
            return {"status": "error", "message": f"Error searching products: {str(e)}"}
        finally:
            conn.close()