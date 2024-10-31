from abc import ABC, abstractmethod

# Interface Class
class BaseModel(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
