from datetime import datetime
from typing import Optional, Dict, Any, Union, Tuple
from .base_model import BaseModel
from .person import Person
from core.lib import db

class Customer(Person):
    def __init__(self, name: str, email: str = "", phone: str = "", address: str = ""):
        super().__init__(name=name)
        self.customer_id: Optional[int] = None
        self.email = email
        self.phone = phone
        self.address = address

    def create(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute(
            '''INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)''',
            (self.name, self.email, self.phone, self.address)
        )
        conn.commit()
        success = cursor.rowcount > 0
        customer_id = cursor.lastrowid if success else None
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Customer '{self.name}' saved successfully." if success else f"Failed to save customer '{self.name}'."
        }
        if success:
            response["data"] = {"customer_id": customer_id}
        
        return response

    def update(self) -> Dict[str, Union[str, Any]]:
        if self.customer_id is None:
            return {"status": "error", "message": "Customer ID is required to update a customer."}

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute(
            '''UPDATE customers SET name = ?, email = ?, phone = ?, address = ? WHERE customer_id = ?''',
            (self.name, self.email, self.phone, self.address, self.customer_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Customer '{self.name}' updated successfully." if success else f"Failed to update customer '{self.name}' or no changes were made."
        }
        
        return response

    def delete(self) -> Dict[str, Union[str, Any]]:
        if self.customer_id is None:
            return {"status": "error", "message": "Customer ID is required to delete a customer."}

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''DELETE FROM customers WHERE customer_id = ?''', (self.customer_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        response = {
            "status": "success" if success else "error",
            "message": f"Customer with ID '{self.customer_id}' deleted successfully." if success else f"Failed to delete customer with ID '{self.customer_id}' or customer does not exist."
        }
        
        return response

    def get_by_id(self, id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''SELECT * FROM customers WHERE customer_id = ?''', (id,))
        customer = cursor.fetchone()
        conn.close()

        response = {
            "status": "success" if customer else "error",
            "message": "Customer retrieved successfully." if customer else f"Customer with ID {id} not found."
        }
        if customer:
            response["data"] = customer
        
        return response

    def get_all(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''SELECT * FROM customers''')
        customers = cursor.fetchall()
        conn.close()

        response = {
            "status": "success",
            "message": "Customers retrieved successfully." if customers else "No customers found."
        }
        if customers:
            response["data"] = customers
        
        return response

    def get_by_phone(self, phone: str) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {"status": "error", "message": "Database connection error."}

        cursor.execute('''SELECT * FROM customers WHERE phone = ?''', (phone,))
        customer = cursor.fetchone()
        conn.close()

        response = {
            "status": "success" if customer else "error",
            "message": "Customer retrieved successfully." if customer else f"Customer with phone '{phone}' not found."
        }
        if customer:
            response["data"] = customer
        
        return response
