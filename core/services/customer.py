from datetime import datetime
from typing import Optional, Tuple, Any
from .base_model import BaseModel
from core.lib import db

class Customer(BaseModel):
    def __init__(self, name: str, email: str = "", phone: str = "", address: str = ""):
        self.customer_id: Optional[int] = None
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)''', 
                       (self.name, self.email, self.phone, self.address))
        conn.commit()
        conn.close()

        return f"Customer {self.name} saved to database." if cursor.rowcount > 0 else f"Failed to save customer {self.name}."

    def update(self) -> str:
        if self.customer_id is None:
            return "Customer ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''UPDATE customers 
                          SET name = ?, email = ?, phone = ?, address = ? 
                          WHERE customer_id = ?''', 
                       (self.name, self.email, self.phone, self.address, self.customer_id))
        conn.commit()
        conn.close()

        return f"Customer {self.name} updated in database." if cursor.rowcount > 0 else f"Failed to update customer {self.name}."

    def delete(self) -> str:
        if self.customer_id is None:
            return "Customer ID is not set."

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return "Database connection error."

        cursor.execute('''DELETE FROM customers WHERE customer_id = ?''', (self.customer_id,))
        conn.commit()
        conn.close()

        return f"Customer {self.name} deleted from database." if cursor.rowcount > 0 else f"Failed to delete customer {self.name}."

    def get_by_id(self, id: int) -> Optional[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return None

        cursor.execute('''SELECT * FROM customers WHERE customer_id = ?''', (id,))
        customer = cursor.fetchone()
        conn.close()
        
        return customer

    def get_all(self):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM customers''')
        customers = cursor.fetchall()
        conn.close()
        
        return customers

    def get_by_phone(self, phone: str) -> Optional[Tuple[Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            print("Database connection error.")
            return None

        cursor.execute('''SELECT * FROM customers WHERE phone = ?''', (phone,))
        customer = cursor.fetchone()
        conn.close()
        
        return customer
