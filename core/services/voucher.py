from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any, Union
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

    def create(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        cursor.execute('''INSERT INTO vouchers (code, discount_value, expiration_date, quota) 
                          VALUES (?, ?, ?, ?)''', 
                       (self.code, float(self.discount_value), self.expiration_date, self.quota))
        conn.commit()
        success = cursor.rowcount > 0
        voucher_id = cursor.lastrowid if success else None
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Voucher '{self.code}' saved successfully." if success else f"Failed to save voucher '{self.code}'."
        }
        if success:
            response["data"] = {"voucher_id": voucher_id}

        return response

    def get_all(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM vouchers ORDER BY voucher_id DESC''')
        vouchers = cursor.fetchall()
        conn.close()

        response = {
            "status": "success",
            "message": "Vouchers retrieved successfully." if vouchers else "No vouchers found."
        }
        if vouchers:
            response["data"] = vouchers

        return response

    def get_by_id(self, id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM vouchers WHERE voucher_id = ?''', (id,))
        voucher = cursor.fetchone()
        conn.close()

        response = {
            "status": "success" if voucher else "error",
            "message": "Voucher retrieved successfully." if voucher else f"Voucher with ID {id} not found."
        }
        if voucher:
            response["data"] = voucher

        return response

    def update(self) -> Dict[str, Union[str, Any]]:
        if self.voucher_id is None:
            return {
                "status": "error",
                "message": "Voucher ID is required to update a voucher."
            }

        conn, cursor = db.init_db()
        cursor.execute('''UPDATE vouchers 
                          SET code = ?, discount_value = ?, expiration_date = ?, quota = ? 
                          WHERE voucher_id = ?''', 
                       (self.code, float(self.discount_value), self.expiration_date, self.quota, self.voucher_id))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Voucher '{self.code}' updated successfully." if success else f"Failed to update voucher '{self.code}' or no changes were made."
        }

        return response

    def delete(self) -> Dict[str, Union[str, Any]]:
        if self.voucher_id is None:
            return {
                "status": "error",
                "message": "Voucher ID is required to delete a voucher."
            }

        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM vouchers WHERE voucher_id = ?''', (self.voucher_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Voucher with ID '{self.voucher_id}' deleted successfully." if success else f"Failed to delete voucher with ID '{self.voucher_id}' or voucher does not exist."
        }

        return response

    def get_by_code(self, code: str) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        current_date = datetime.now().date()
        cursor.execute('''SELECT v.voucher_id, v.code, v.quota, v.discount_value, v.expiration_date, 
                                 COUNT(t.voucher_id) as used_quota
                          FROM vouchers v
                          LEFT JOIN transactions t ON v.voucher_id = t.voucher_id
                          WHERE v.code = ? AND v.expiration_date > ? 
                          GROUP BY v.voucher_id
                          HAVING used_quota < v.quota OR v.quota IS NULL
                       ''', (code, current_date))
        voucher = cursor.fetchone()
        conn.close()

        response = {
            "status": "success" if voucher else "error",
            "message": "Voucher retrieved successfully." if voucher else f"Voucher with code '{code}' not found."
        }
        if voucher:
            response["data"] = voucher

        return response

    def get_all_by_code(self, code: str) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM vouchers WHERE code = ? ORDER BY voucher_id DESC''', (code,))
        vouchers = cursor.fetchall()
        conn.close()

        response = {
            "status": "success",
            "message": "Vouchers retrieved successfully." if vouchers else "No vouchers found."
        }
        if vouchers:
            response["data"] = vouchers

        return response
