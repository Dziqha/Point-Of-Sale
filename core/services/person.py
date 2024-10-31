from datetime import datetime
from .base_model import BaseModel

class Person(BaseModel):
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()
    
    def create(self):
        pass

    def get_all(self):
        pass

    def get_by_id(self, id):
        pass

    def update(self):
        pass

    def delete(self):
        pass
