from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from .base_model import BaseModel
from core.lib import db

class Voucher(BaseModel):
    def __init__(self, code: str, discount_value: Decimal, expiration_date: datetime, quota: Optional[int] = None):
        self.voucher_id: Optional[int] = None
        self.code = code
        self.discount_value = discount_value
        self.expiration_date = expiration_date
        self.quota = quota
        self.created_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''INSERT INTO vouchers (code, discount_value, expiration_date, quota) 
                          VALUES (?, ?, ?, ?)''', 
                       (self.code, float(self.discount_value), self.expiration_date, self.quota))
        conn.commit()
        conn.close()

        return f"Voucher {self.code} saved to database." if cursor.rowcount > 0 else f"Failed to save voucher {self.code}."
    
    def update(self) -> str:
        if self.voucher_id is None:
            return "Voucher ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''UPDATE vouchers 
                        SET code = ?, discount_value = ?, expiration_date = ?, quota = ? 
                        WHERE voucher_id = ?''', 
                    (self.code, float(self.discount_value), self.expiration_date, self.quota, self.voucher_id))
        conn.commit()
        conn.close()

        return f"Voucher {self.code} updated in database." if cursor.rowcount > 0 else f"Failed to update voucher {self.code}."

    def delete(self) -> None:
        if self.voucher_id is None:
            return "Voucher ID is not set."
        
        conn, cursor = db.init_db()
        
        cursor.execute('''DELETE FROM vouchers WHERE voucher_id = ?''', (self.voucher_id,))
        conn.commit()
        conn.close()
        return f"Voucher {self.code} deleted from database."
    
    def apply_voucher(self, transaction) -> None:
        if transaction.paid_amount > 0:
            print("Cannot apply voucher to an already paid transaction.")
            return

        if self.quota is not None and self.quota <= 0:
            print(f"Voucher {self.code} is no longer valid due to quota exhaustion.")
            return

        if self.discount_value > transaction.total:
            print(f"Discount exceeds the total amount. Applying maximum possible discount of {transaction.total}.")
            transaction.total = 0  
        else:
            transaction.total -= self.discount_value
        
        if self.quota is not None:
            self.quota -= 1

        transaction.create() 
        print(f"Voucher {self.code} applied to transaction. New total: {transaction.total:.2f}")

    def get_by_id(self, id: int) -> Optional[Tuple]:
        conn, cursor = db.init_db()

        cursor.execute('''SELECT * FROM vouchers WHERE voucher_id = ?''', (id,))
        voucher = cursor.fetchone()
        conn.close()
        return voucher

    def get_by_code(self, code: str) -> Optional[Tuple]:
        conn, cursor = db.init_db()

        current_date = datetime.now().date()

        cursor.execute('''
        SELECT v.voucher_id, v.code, v.quota, v.discount_value, v.expiration_date, 
            COUNT(t.voucher_id) as used_quota
        FROM vouchers v
        LEFT JOIN transactions t ON v.voucher_id = t.voucher_id
        WHERE v.code = ? AND v.expiration_date > ? 
        GROUP BY v.voucher_id
        HAVING used_quota < v.quota OR v.quota IS NULL
        ''', (code, current_date))

        voucher = cursor.fetchone()
        conn.close()
        return voucher
    
    def get_all(self) -> List[Tuple]:
        conn, cursor = db.init_db()

        cursor.execute('''SELECT * FROM vouchers''')
        vouchers = cursor.fetchall()
        conn.close()
        return vouchers
