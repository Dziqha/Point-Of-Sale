from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Any
from .base_model import BaseModel
from core.lib import db

class Promo(BaseModel):
    def __init__(self, product_id: Optional[int] = None, name: str = "", description: str = "", discount_percentage: Decimal = Decimal(0), start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        self.promo_id: Optional[int] = None
        self.product_id = product_id
        self.name = name
        self.description = description
        self.discount_percentage = discount_percentage
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = datetime.now()

    def create(self):
        con, cursor = db.init_db()

        cursor.execute('''
            INSERT INTO promos (product_id, name, description, discount_percentage, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.product_id,
            self.name,
            self.description,
            float(self.discount_percentage),
            self.start_date,
            self.end_date
        ))

        con.commit()

        return f"Promo {self.name} saved to database." if cursor.rowcount > 0 else f"Failed to save promo {self.name}."

    def update(self) -> str:
        if self.promo_id is None:
            return "Promo ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''UPDATE promos 
                          SET product_id = ?, name = ?, description = ?, discount_percentage = ?, start_date = ?, end_date = ? 
                          WHERE promo_id = ?''', 
                       (self.product_id, self.name, self.description, float(self.discount_percentage), self.start_date, self.end_date, self.promo_id))
        conn.commit()
        conn.close()

        return f"Promo {self.name} updated in database." if cursor.rowcount > 0 else f"Failed to update promo {self.name}."

    def delete(self) -> str:
        if self.promo_id is None:
            return "Promo ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''DELETE FROM promos WHERE promo_id = ?''', (self.promo_id,))
        conn.commit()
        conn.close()

        return f"Promo {self.name} deleted from database." if cursor.rowcount > 0 else f"Failed to delete promo {self.name}."

    def get_by_id(self, id: int) -> Optional[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return None

        cursor.execute('''SELECT * FROM promos WHERE promo_id = ?''', (id,))
        promo = cursor.fetchone()
        conn.close()
        
        return promo

    def get_all(self) -> List[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return []

        cursor.execute('''SELECT * FROM promos''')
        promos = cursor.fetchall()
        conn.close()
        
        return promos
