from decimal import Decimal
from typing import Optional
from .base_model import BaseModel

class TransactionItem(BaseModel):
    def __init__(self, transaction_id: int, product_id: int, quantity: int, price: Decimal, discount: Decimal, total: Decimal):
        self.transaction_item_id: Optional[int] = None
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.total = total

    def save(self):
        # Implementation to save transaction item to database
        pass

    def delete(self):
        # Implementation to delete transaction item from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve transaction item by ID
        pass
