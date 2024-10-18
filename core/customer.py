from datetime import datetime
from typing import Optional
from .base_model import BaseModel

class Customer(BaseModel):
    def __init__(self, name: str, email: str = "", phone: str = "", address: str = ""):
        self.customer_id: Optional[int] = None
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = datetime.now()

    def save(self):
        # Implementation to save customer to database
        pass

    def delete(self):
        # Implementation to delete customer from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve customer by ID
        pass
