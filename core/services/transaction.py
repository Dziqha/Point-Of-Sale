from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from core.lib import db

class Transaction(BaseModel):
    def __init__(self, user_id: int, customer_id: int, total: float, discount: float, final_total: float, paid_amount: float, return_amount: float, voucher_id: Optional[int] = None):
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

    def create(self) -> dict:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        try:
            cursor.execute('''INSERT INTO transactions (user_id, customer_id, total, discount, final_total, paid_amount, return_amount, voucher_id, created_at) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (self.user_id, self.customer_id, self.total, self.discount, self.final_total, self.paid_amount, self.return_amount, self.voucher_id, self.created_at))
            conn.commit()
            if cursor.rowcount > 0:
                self.transaction_id = cursor.lastrowid
                return {
                    "status": "success",
                    "message": f"Transaction with ID {self.transaction_id} saved to database.",
                    "transaction_id": self.transaction_id
                }
            else:
                return {"status": "error", "message": "Failed to save transaction."}
        except Exception as e:
            return {"status": "error", "message": f"Error creating transaction: {str(e)}"}
        finally:
            conn.close()

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
            print("Database error: Koneksi database gagal.")
            return None

        try:
            cursor.execute('''
                SELECT t.*, u.username as cashier_name, c.phone as customer_phone
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.user_id
                LEFT JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.transaction_id = ?
            ''', (id,))
            transaction = cursor.fetchone()
            return transaction
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> List[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database error: Koneksi database gagal.")
            return []

        try:
            cursor.execute('''
                SELECT t.*, u.username as cashier_name, c.phone as customer_phone
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.user_id
                LEFT JOIN customers c ON t.customer_id = c.customer_id
                ORDER BY t.transaction_id DESC
            ''')
            transactions = cursor.fetchall()
            return transactions
        except Exception as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    def get_by_user_id(self, user_id: int) -> List[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return []

        cursor.execute('''SELECT * FROM transactions WHERE user_id = ?''', (user_id,))
        transactions = cursor.fetchall()
        conn.close()

        return transactions
