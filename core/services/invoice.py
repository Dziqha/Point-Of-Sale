from datetime import datetime
from typing import Optional
from .base_model import BaseModel
from core.lib import db

class Invoice(BaseModel):
    def __init__(self, transaction_id: int, invoice_number: str):
        self.invoice_id: Optional[int] = None
        self.transaction_id = transaction_id
        self.invoice_number = invoice_number
        self.issued_at = datetime.now()

    def create(self) -> str:
        conn, cursor = db.init_db()
        cursor.execute('''INSERT INTO invoices (transaction_id, invoice_number, issued_at) 
                          VALUES (?, ?, ?)''', 
                       (self.transaction_id, self.invoice_number, self.issued_at))
        self.invoice_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return f"Invoice {self.invoice_number} created successfully."

    def get_all(self):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM invoices''')
        invoices = cursor.fetchall()
        conn.close()
        return invoices

    def get_by_id(self, invoice_id: int):
        conn, cursor = db.init_db()
        cursor.execute('''SELECT * FROM invoices WHERE invoice_id = ?''', (invoice_id,))
        invoice = cursor.fetchone()
        conn.close()
        return invoice

    def update(self) -> str:
        if self.invoice_id is None:
            raise ValueError("Invoice ID is required to update an invoice.")
        
        conn, cursor = db.init_db()
        cursor.execute('''UPDATE invoices SET transaction_id = ?, invoice_number = ?, issued_at = ? 
                          WHERE invoice_id = ?''', 
                       (self.transaction_id, self.invoice_number, self.issued_at, self.invoice_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return f"Invoice {self.invoice_number} updated successfully."
        else:
            return f"No changes made to invoice {self.invoice_number}."

    def delete(self) -> str:
        if self.invoice_id is None:
            raise ValueError("Invoice ID is required to delete an invoice.")

        conn, cursor = db.init_db()
        cursor.execute('''DELETE FROM invoices WHERE invoice_id = ?''', (self.invoice_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows > 0:
            return f"Invoice {self.invoice_number} deleted successfully."
        else:
            return f"Failed to delete invoice {self.invoice_number} or invoice does not exist."
