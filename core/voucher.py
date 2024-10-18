from datetime import datetime
from decimal import Decimal
from typing import Optional
from .base_model import BaseModel

class Voucher(BaseModel):
    def __init__(self, code: str, discount_value: Decimal, expiration_date: datetime):
        self.voucher_id: Optional[int] = None
        self.code = code
        self.discount_value = discount_value
        self.expiration_date = expiration_date
        self.created_at = datetime.now()

    def save(self):
        # Implementation to save voucher to database
        pass

    def delete(self):
        # Implementation to delete voucher from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve voucher by ID
        pass
