from datetime import datetime
from typing import Optional
from .base_model import BaseModel
from core.lib import db

class StockMovement(BaseModel):
    def __init__(self, product_id: int, user_id: int, movement_type: str, quantity_change: int, reason: str = ""):
        self.movement_id: Optional[int] = None
        self.product_id = product_id
        self.user_id = user_id
        self.movement_type = movement_type
        self.quantity_change = quantity_change
        self.reason = reason
        self.created_at = datetime.now()

    def create(self):
        conn, cursor = db.init_db()

        cursor.execute('''INSERT INTO stock_movements (product_id, user_id, movement_type, quantity_change, reason, created_at)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (self.product_id, self.user_id, self.movement_type, self.quantity_change, self.reason, self.created_at))
        
        if self.movement_type == 'in':
            cursor.execute('''UPDATE products SET stock = stock + ? WHERE product_id = ?''',
                           (self.quantity_change, self.product_id))
        elif self.movement_type == 'out':
            cursor.execute('''UPDATE products SET stock = stock - ? WHERE product_id = ?''',
                           (self.quantity_change, self.product_id))

        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        if affected_rows > 0:
            return f"Stock movement for product ID {self.product_id} created successfully and stock updated."
        else:
            return f"Failed to create stock movement for product ID {self.product_id}."

    def get_all(self):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM stock_movements ORDER BY movement_id DESC;''')
        movements = cursor.fetchall()
        conn.close()
        return movements
    
    def get_by_id(self, movement_id: int):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM stock_movements WHERE movement_id = ?''', (movement_id,))
        movement = cursor.fetchone()
        conn.close()
        return movement

    def update(self):
        if self.movement_id is None:
            raise ValueError("Movement ID is required to update a stock movement.")
        
        conn, cursor = db.init_db()
        cursor.execute('''UPDATE stock_movements 
                          SET product_id = ?, user_id = ?, movement_type = ?, 
                              quantity_change = ?, reason = ?
                          WHERE movement_id = ?''',
                       (self.product_id, self.user_id, self.movement_type,
                        self.quantity_change, self.reason, self.movement_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        if affected_rows > 0:
            return f"Stock movement ID {self.movement_id} updated successfully."
        else:
            return f"Failed to update stock movement ID {self.movement_id} or it does not exist."
        
    def delete(self):
        if self.movement_id is None:
            raise ValueError("Movement ID is required to delete a stock movement.")
        
        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM stock_movements WHERE movement_id = ?''', (self.movement_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        if affected_rows > 0:
            return f"Stock movement ID {self.movement_id} deleted successfully."
        else:
            return f"Failed to delete stock movement ID {self.movement_id} or it does not exist."

    def get_by_product_id(self, product_id: int):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM stock_movements WHERE product_id = ? ORDER BY movement_id DESC''', (product_id,))
        movements = cursor.fetchall()
        conn.close()
        return movements
