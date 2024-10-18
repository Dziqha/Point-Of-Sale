from datetime import datetime
from decimal import Decimal
from typing import Optional
from .base_model import BaseModel

class Promo(BaseModel):
    def __init__(self, name: str, description: str, discount_percentage: Decimal, start_date: datetime, end_date: datetime):
        self.promo_id: Optional[int] = None
        self.name = name
        self.description = description
        self.discount_percentage = discount_percentage
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = datetime.now()

    def save(self):
        # Implementation to save promo to database
        pass

    def delete(self):
        # Implementation to delete promo from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve promo by ID
        pass
