from datetime import datetime
from typing import Optional, Dict, Any, Union
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

    def create(self) -> Dict[str, Union[str, Any]]:
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
        success = cursor.rowcount > 0
        self.movement_id = cursor.lastrowid if success else None

        conn.close()
        response = {
            "status": "success" if success else "failed",
            "message": "Stock movement created successfully." if success else "Failed to create stock movement."
        }

        if success:
            response["data"] = {"movement_id": self.movement_id}

        return response
    def get_all(self)-> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''
            SELECT sm.*, p.name AS product_name, p.sku, u.username AS admin_username
            FROM stock_movements sm
            JOIN products p ON sm.product_id = p.product_id
            JOIN users u ON sm.user_id = u.user_id
            ORDER BY sm.movement_id DESC
        ''')
        movements = cursor.fetchall()
        conn.close()
        response = {
            "status": "success" if  movements else "failed",
            "message": "Stock movements found" if movements else "Failed to find stock movements"
        }

        if movements:
            response["data"] = movements

        return response

    def get_by_id(self, movement_id: int)-> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''
            SELECT sm.*, p.name AS product_name, p.sku, u.username AS admin_username
            FROM stock_movements sm
            JOIN products p ON sm.product_id = p.product_id
            JOIN users u ON sm.user_id = u.user_id
            WHERE sm.movement_id = ?
        ''', (movement_id,))
        movement = cursor.fetchone()
        conn.close()
        response = {
            "status": "success" if movement else "failed",
            "message": "Stock movement found" if movement else "Failed to find stock movement"
        }

        if movement:
            response["data"] = movement

        return response

    def update(self)-> Dict[str, Union[str, Any]]:
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
        success = cursor.rowcount > 0
        conn.close()
        
        response = {
            "status": "success" if success else "failed",
            "message": "Stock movement updated successfully." if success else "Failed to update stock movement."
        }
        
        return response
    def delete(self)-> Dict[str, Union[str, Any]]:
        if self.movement_id is None:
            raise ValueError("Movement ID is required to delete a stock movement.")
        
        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM stock_movements WHERE movement_id = ?''', (self.movement_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        response = {
            "status": "success" if success else "failed",
            "message": "Stock movement deleted successfully." if success else "Failed to delete stock movement."
        }
        
        return response
    def get_by_product_id(self, product_id: int)-> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''
            SELECT sm.*, p.name AS product_name, p.sku, u.username AS admin_username
            FROM stock_movements sm
            JOIN products p ON sm.product_id = p.product_id
            JOIN users u ON sm.user_id = u.user_id
            WHERE sm.product_id = ?
            ORDER BY sm.movement_id DESC
        ''', (product_id,))
        movements = cursor.fetchall()
        conn.close()

        response = {
            "status": "success" if movements else "failed",
            "message": "Stock movements found" if movements else "Failed to find stock movements"
        }

        if movements:
            response["data"] = movements

        return response
