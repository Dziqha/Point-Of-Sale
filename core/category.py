from datetime import datetime
from typing import Optional
from .base_model import BaseModel

class Category(BaseModel):
    def __init__(self, name: str, description: str = ""):
        self.category_id: Optional[int] = None
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    def save(self):
        # Implementation to save category to database
        pass

    def delete(self):
        # Implementation to delete category from database
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implementation to retrieve category by ID
        pass
