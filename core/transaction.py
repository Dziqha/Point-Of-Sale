from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from lib import db

class Transaction(BaseModel):
    def __init__(self, user_id: int, customer_id: int, total: Decimal, discount: Decimal, final_total: Decimal, paid_amount: Decimal, return_amount: Decimal, voucher_id: Optional[int] = None):
        self.transaction_id: Optional[int] = None
        self.user_id = user_id
        self.customer_id = customer_id
        self.total = total
        self.discount = discount
        self.final_total = final_total
        self.paid_amount = paid_amount
        self.return_amount = return_amount
        self.voucher_id = voucher_id
        self.created_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''INSERT INTO transactions (user_id, customer_id, total, discount, final_total, paid_amount, return_amount, voucher_id, created_at) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (self.user_id, self.customer_id, self.total, self.discount, self.final_total, self.paid_amount, self.return_amount, self.voucher_id, self.created_at))
        conn.commit()
        if cursor.rowcount > 0:
            self.transaction_id = cursor.lastrowid
            result = f"Transaction with ID {self.transaction_id} saved to database."
        else:
            result = "Failed to save transaction."
        
        conn.close()
        return result

    def delete(self) -> str:
        if self.transaction_id is None:
            return "Transaction ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''DELETE FROM transactions WHERE transaction_id = ?''', (self.transaction_id,))
        conn.commit()
        result = f"Transaction with ID {self.transaction_id} deleted from database." if cursor.rowcount > 0 else "Failed to delete transaction."
        conn.close()

        return result

    def update(self) -> str:
        if self.transaction_id is None:
            return "Transaction ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''UPDATE transactions 
                          SET total = ?, discount = ?, final_total = ?, paid_amount = ?, return_amount = ?, voucher_id = ? 
                          WHERE transaction_id = ?''', 
                       (self.total, self.discount, self.final_total, self.paid_amount, self.return_amount, self.voucher_id, self.transaction_id))
        conn.commit()
        result = f"Transaction with ID {self.transaction_id} updated in database." if cursor.rowcount > 0 else "Failed to update transaction."
        conn.close()

        return result

    def get_by_id(self, id: int) -> Optional[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return None

        cursor.execute('''SELECT * FROM transactions WHERE transaction_id = ?''', (id,))
        transaction = cursor.fetchone()
        conn.close()
        
        return transaction

    def get_all(self) -> List[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return []

        cursor.execute('''SELECT * FROM transactions''')
        transactions = cursor.fetchall()
        conn.close()
        
        return transactions

    def get_by_user_id(self, user_id: int) -> List[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return []

        cursor.execute('''SELECT * FROM transactions WHERE user_id = ?''', (user_id,))
        transactions = cursor.fetchall()
        conn.close()

        return transactions
