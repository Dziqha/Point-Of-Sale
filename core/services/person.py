from datetime import datetime

class Person:
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()
