from datetime import datetime
from decimal import Decimal
from typing import Optional
from .base_model import BaseModel

class Product(BaseModel):
    def __init__(self, name: str, sku: str, category_id: int, price: Decimal, description: str = ""):
        self.product_id: Optional[int] = None
        self.name = name
        self.sku = sku
        self.category_id = category_id
        self.stock = 0
        self.price = price
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        # Implementation to save product to database
        pass

    def delete(self):
        # Implementation to delete product from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve product by ID
        pass
