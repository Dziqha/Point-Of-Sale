# models.py
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def register(self):
        pass


class Item(ABC):
    def __init__(self, name, price, quantity, description, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.category = category
    
    @abstractmethod
    def display_item(self):
        pass

class Product(Item):
    def __init__(self, name, price, stock, description, category):
        super().__init__(name, price, stock, description, category)
        self.discount = 0

    def display_item(self):
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")
        print(f"Description: {self.description}")
        print(f"Category: {self.category}")

    def update_stock(self, quantity):
        self.stock -= quantity
        print(f"Stock updated: {self.stock}")

    def add_stock(self, quantity):
        self.stock += quantity
        print(f"Stock added: {self.stock}")

    def remove_stock(self, quantity):
        self.stock -= quantity
        print(f"Stock removed: {self.stock}")

    def set_discount(self, discount):
        if discount < 0 or discount > 100:
            print("Invalid discount value. Discount must be between 0 and 100.")
        else:
            self.discount = discount
            print(f"Discount set to: {self.discount}%")

    def get_price_after_discount(self):
        return self.price * (1 - self.discount / 100)

class Voucher(Product):
    def __init__(self, code, discount_amount):
        self.code = code
        self.discount_amount = discount_amount

    def apply_voucher(self, transaction):
        transaction.total -= self.discount_amount
        print(f"Voucher applied. New total: ${transaction.total:.2f}")
