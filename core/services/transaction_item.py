from decimal import Decimal
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from core.lib import db

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
            conn.execute('BEGIN;')

            # 1. Fetch product price and discount
            cursor.execute('''SELECT 
                                p.price, 
                                IFNULL(pr.discount_percentage, 0) AS discount_percentage
                            FROM 
                                products p
                            LEFT JOIN 
                                (SELECT product_id, discount_percentage 
                                FROM promos
                                WHERE start_date <= CURRENT_DATE AND end_date >= CURRENT_DATE
                                ) pr 
                            ON 
                                p.product_id = pr.product_id
                            WHERE 
                                p.product_id = ?;
                ''', (self.product_id,))
            product = cursor.fetchone()

            if not product:
                return {"status": "error", "message": "Product not found."}

            price = product[0]
            discount_percentage = product[1]

            # 2. Calculate discount and total
            discount_amount = price * (discount_percentage / 100)
            final_price = price - discount_amount
            total = final_price * self.quantity

            # 3. Insert into transaction_items
            cursor.execute('''INSERT INTO transaction_items (transaction_id, product_id, price, discount, quantity, total)
                            VALUES (?, ?, ?, ?, ?, ?);
                ''', (self.transaction_id, self.product_id, price, discount_percentage, self.quantity, total))

            # 4. Update stock
            cursor.execute('''UPDATE products
                            SET stock = stock - ?
                            WHERE product_id = ? AND stock >= ?;
                ''', (self.quantity, self.product_id, self.quantity))

            conn.commit()

            if cursor.rowcount > 0:
                return {"status": "success", "message": "Transaction item saved to database and stock updated."}
            else:
                return {"status": "error", "message": "Failed to save transaction item or product not found."}

        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
        
        finally:
            conn.close()

    def delete(self) -> str:
        if self.transaction_item_id is None:
            return "Transaction item ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''DELETE FROM transaction_items WHERE transaction_item_id = ?''', (self.transaction_item_id,))
        conn.commit()
        result = f"Transaction item with ID {self.transaction_item_id} deleted from database." if cursor.rowcount > 0 else "Failed to delete transaction item."
        conn.close()

        return result

    def get_by_id(self, id: int) -> Optional[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return None

        cursor.execute('''SELECT * FROM transaction_items WHERE transaction_item_id = ?''', (id,))
        transaction_item = cursor.fetchone()
        conn.close()
        
        return transaction_item

    def get_all_by_transaction_id(self, transaction_id: int) -> List[Tuple[Any]]:
            conn, cursor = db.init_db()
            if conn is None or cursor is None:
                print("Database connection error.")
                return []

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

            return transaction_items

    def update(self) -> str:
        if self.transaction_item_id is None:
            return "Transaction item ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''UPDATE transaction_items 
                          SET product_id = ?, quantity = ?, price = ?, discount = ?, total = ? 
                          WHERE transaction_item_id = ?''', 
                       (self.product_id, self.quantity, self.price, self.discount, self.total, self.transaction_item_id))
        conn.commit()
        result = f"Transaction item with ID {self.transaction_item_id} updated in database." if cursor.rowcount > 0 else "Failed to update transaction item."
        conn.close()

        return result
    
    def get_all(self):
        pass
