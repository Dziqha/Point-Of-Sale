from decimal import Decimal
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from core.lib import db
from datetime import datetime

class TransactionItem(BaseModel):
    def __init__(self, transaction_id: int, product_id: int, quantity: int, price: Decimal, discount: Decimal, total: Decimal):
        self.transaction_item_id: Optional[int] = None
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.total = total

    def create(self) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            now = datetime.now()

            conn.execute('BEGIN;')

            # 1. Fetch product price and stock
            cursor.execute('''
                SELECT price, stock
                FROM products
                WHERE product_id = ?;
            ''', (self.product_id,))
            product = cursor.fetchone()

            if not product:
                return {"status": "error", "message": "Product not found."}

            price = product[0]
            stock = product[1]

            if stock < self.quantity:
                return {"status": "error", "message": "Insufficient stock."}

            # 2. Fetch discount percentage (if available)
            cursor.execute('''
                SELECT IFNULL(discount_percentage, 0) AS discount_percentage
                FROM promos
                WHERE product_id = ?
                AND start_date <= ?
                AND end_date >= ?;
            ''', (self.product_id, now, now))
            discount = cursor.fetchone()

            discount_percentage = discount[0] if discount else 0

            # 3. Calculate discount and total
            discount_amount = price * (discount_percentage / 100)
            final_price = price - discount_amount
            total = final_price * self.quantity

            # 4. Insert into transaction_items
            cursor.execute('''
                INSERT INTO transaction_items (transaction_id, product_id, price, discount, quantity, total)
                VALUES (?, ?, ?, ?, ?, ?);
            ''', (self.transaction_id, self.product_id, price, discount_percentage, self.quantity, total))

            # 5. Update stock
            cursor.execute('''
                UPDATE products
                SET stock = stock - ?
                WHERE product_id = ? AND stock >= ?;
            ''', (self.quantity, self.product_id, self.quantity))

            conn.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": "Transaction item saved to database and stock updated.",
                    "data": {
                        "transaction_item_id": cursor.lastrowid,
                        "transaction_id": self.transaction_id,
                        "product_id": self.product_id,
                        "quantity": self.quantity,
                        "price": str(price),
                        "discount": str(discount_percentage),
                        "total": str(total)
                    }
                }
            else:
                return {"status": "error", "message": "Failed to save transaction item or product not found."}

        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

        finally:
            conn.close()

    def delete(self) -> dict:
        if self.transaction_item_id is None:
            return {"status": "error", "message": "Transaction item ID is not set."}

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''DELETE FROM transaction_items WHERE transaction_item_id = ?''', (self.transaction_item_id,))
        conn.commit()
        result = {
            "status": "success" if cursor.rowcount > 0 else "error",
            "message": f"Transaction item with ID {self.transaction_item_id} deleted from database." if cursor.rowcount > 0 else "Failed to delete transaction item."
        }
        conn.close()

        return result

    def get_by_id(self, id: int) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''SELECT * FROM transaction_items WHERE transaction_item_id = ?''', (id,))
        transaction_item = cursor.fetchone()
        conn.close()

        if transaction_item:
            return {
                "status": "success",
                "message": "Transaction item found.",
                "data": {
                    "transaction_item_id": transaction_item[0],
                    "transaction_id": transaction_item[1],
                    "product_id": transaction_item[2],
                    "price": str(transaction_item[3]),
                    "discount": str(transaction_item[4]),
                    "quantity": transaction_item[5],
                    "total": str(transaction_item[6])
                }
            }
        else:
            return {"status": "error", "message": "Transaction item not found."}

    def get_all_by_transaction_id(self, transaction_id: int) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''
            SELECT 
                ti.transaction_item_id,
                ti.transaction_id,
                ti.product_id,
                p.name AS product_name,
                p.sku AS product_sku,
                ti.quantity,
                ti.price,
                ti.discount,
                ti.total
            FROM 
                transaction_items ti
            JOIN 
                products p ON ti.product_id = p.product_id
            WHERE 
                ti.transaction_id = ?
        ''', (transaction_id,))
        transaction_items = cursor.fetchall()
        conn.close()

        if transaction_items:
            return {
                "status": "success",
                "message": "Transaction items found.",
                "data": [
                    {
                        "transaction_item_id": row[0],
                        "transaction_id": row[1],
                        "product_id": row[2],
                        "product_name": row[3],
                        "product_sku": row[4],
                        "quantity": row[5],
                        "price": str(row[6]),
                        "discount": str(row[7]),
                        "total": str(row[8])
                    } for row in transaction_items
                ]
            }
        else:
            return {"status": "error", "message": "No transaction items found for the given transaction ID."}

    def update(self) -> dict:
        if self.transaction_item_id is None:
            return {"status": "error", "message": "Transaction item ID is not set."}

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''UPDATE transaction_items 
                          SET product_id = ?, quantity = ?, price = ?, discount = ?, total = ? 
                          WHERE transaction_item_id = ?''', 
                       (self.product_id, self.quantity, self.price, self.discount, self.total, self.transaction_item_id))
        conn.commit()
        result = {
            "status": "success" if cursor.rowcount > 0 else "error",
            "message": f"Transaction item with ID {self.transaction_item_id} updated in database." if cursor.rowcount > 0 else "Failed to update transaction item."
        }
        conn.close()

        return result
    
    def get_all(self):
        pass