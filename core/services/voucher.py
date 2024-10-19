from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from .base_model import BaseModel
from core.lib import db

class Voucher(BaseModel):
    def __init__(self, code: str, discount_value: Decimal, expiration_date: datetime):
        self.voucher_id: Optional[int] = None
        self.code = code
        self.discount_value = discount_value
        self.expiration_date = expiration_date
        self.created_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''INSERT INTO vouchers (code, discount_value, expiration_date) 
                          VALUES (?, ?, ?)''', 
                       (self.code, self.discount_value, self.expiration_date))
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
                        SET code = ?, discount_value = ?, expiration_date = ? 
                        WHERE voucher_id = ?''', 
                    (self.code, self.discount_value, self.expiration_date, self.voucher_id))
        conn.commit()
        conn.close()

        return f"Voucher {self.code} updated in database." if cursor.rowcount > 0 else f"Failed to update voucher {self.code}."

    def delete(self) -> None:
        if self.voucher_id is None:
            print("Voucher ID is not set.")
            return
        
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return
        
        cursor.execute('''DELETE FROM vouchers WHERE voucher_id = ?''', (self.voucher_id,))
        conn.commit()
        conn.close()
        print(f"Voucher {self.code} deleted from database.")
    
    def apply_voucher(self, transaction) -> None:
        if transaction.paid_amount > 0:
            print("Cannot apply voucher to an already paid transaction.")
            return

        if self.discount_value > transaction.total:
            print(f"Discount exceeds the total amount. Applying maximum possible discount of {transaction.total}.")
            transaction.total = 0  
        else:
            transaction.total -= self.discount_value

        transaction.create() 
        print(f"Voucher {self.code} applied to transaction. New total: {transaction.total:.2f}")

    def get_by_id(self, id: int) -> Optional[Tuple]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return None

        cursor.execute('''SELECT * FROM vouchers WHERE voucher_id = ?''', (id,))
        voucher = cursor.fetchone()
        conn.close()
        return voucher
    
    def get_all(self) -> List[Tuple]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return []

        cursor.execute('''SELECT * FROM vouchers''')
        vouchers = cursor.fetchall()
        conn.close()
        return vouchers
