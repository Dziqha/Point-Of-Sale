from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def create(self):
        """Saves a new instance of the model to the database."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieves all instances of the model from the database."""
        pass

    @abstractmethod
    def get_by_id(self, id):
        """Retrieves a single instance of the model by its ID."""
        pass

    @abstractmethod
    def update(self):
        """Updates an existing instance of the model in the database."""
        pass

    @abstractmethod
    def delete(self):
        """Deletes an instance of the model from the database."""
        pass
