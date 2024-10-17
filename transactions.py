# transactions.py
from models import Product

class Transaction:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item: Product, quantity):
        self.items.append((item, quantity))
        self.total += item.price * quantity

    def remove_item(self, item: Product):
        for i, (itm, qty) in enumerate(self.items):
            if itm == item:
                self.total -= itm.price * qty
                self.items.pop(i)
                break

    def calculate_total(self):
        return self.total

    def process_payment(self, amount):
        if amount >= self.total:
            return "Payment successful"
        return "Insufficient funds"

class Invoice(Transaction):
    def __init__(self, transaction):
        self.transaction = transaction

    def generate_invoice(self):
        invoice_data = f"Invoice for Transaction:\n"
        invoice_data += "-" * 30 + "\n"
        for item, qty in self.transaction.items:
            invoice_data += f"{item.name} (x{qty}): ${item.price:.2f} each\n"
            invoice_data += f"Total: ${item.price * qty:.2f}\n"
        invoice_data += "-" * 30 + "\n"
        invoice_data += f"Total Amount Due: ${self.transaction.calculate_total():.2f}\n"
        return invoice_data

    def print_invoice(self):
        invoice = self.generate_invoice()
        print(invoice)

class Promotion:
    def __init__(self, description, discount_percentage):
        self.description = description
        self.discount_percentage = discount_percentage

    def apply_promotion(self, item: Product):
        item.set_discount(self.discount_percentage)

    def remove_promotion(self, item: Product):
        item.set_discount(0)
