from decimal import Decimal
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from lib import db

class TransactionItem(BaseModel):
    def __init__(self, transaction_id: int, product_id: int, quantity: int, price: Decimal, discount: Decimal, total: Decimal):
        self.transaction_item_id: Optional[int] = None
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.total = total

    def create(self) -> str:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''INSERT INTO transaction_items (transaction_id, product_id, quantity, price, discount, total) 
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                       (self.transaction_id, self.product_id, self.quantity, self.price, self.discount, self.total))
        conn.commit()
        if cursor.rowcount > 0:
            self.transaction_item_id = cursor.lastrowid
            result = f"Transaction item with ID {self.transaction_item_id} saved to database."
        else:
            result = "Failed to save transaction item."

        conn.close()
        return result

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

        cursor.execute('''SELECT * FROM transaction_items WHERE transaction_id = ?''', (transaction_id,))
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
