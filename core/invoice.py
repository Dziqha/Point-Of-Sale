from datetime import datetime
from typing import Optional
from .base_model import BaseModel

class Invoice(BaseModel):
    def __init__(self, transaction_id: int, invoice_number: str):
        self.invoice_id: Optional[int] = None
        self.transaction_id = transaction_id
        self.invoice_number = invoice_number
        self.issued_at = datetime.now()

    def save(self):
        # Implementation to save invoice to database
        pass

    def delete(self):
        # Implementation to delete invoice from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve invoice by ID
        pass
