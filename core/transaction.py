from datetime import datetime
from decimal import Decimal
from typing import Optional
from .base_model import BaseModel

class Transaction(BaseModel):
    def __init__(self, user_id: int, customer_id: int, total: Decimal, discount: Decimal, final_total: Decimal, paid_amount: Decimal, return_amount: Decimal, voucher_id: Optional[int] = None):
        self.transaction_id: Optional[int] = None
        self.user_id = user_id
        self.customer_id = customer_id
        self.total = total
        self.discount = discount
        self.final_total = final_total
        self.paid_amount = paid_amount
        self.return_amount = return_amount
        self.voucher_id = voucher_id
        self.created_at = datetime.now()

    def save(self):
        # Implementation to save transaction to database
        pass

    def delete(self):
        # Implementation to delete transaction from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve transaction by ID
        pass
