import eel
from decimal import Decimal
from core.services.transaction_item import TransactionItem

@eel.expose
def create_transaction_item(transaction_id: int, product_id: int, quantity: int, price: float, discount: float, total: float):
    transaction_item = TransactionItem(
        transaction_id=transaction_id,
        product_id=product_id,
        quantity=quantity,
        price=Decimal(price),
        discount=Decimal(discount),
        total=Decimal(total)
    )
    return transaction_item.create()

@eel.expose
def update_transaction_item(transaction_item_id: int, product_id: int, quantity: int, price: float, discount: float, total: float):
    transaction_item = TransactionItem(
        transaction_id=0,
        product_id=product_id,
        quantity=quantity,
        price=Decimal(price),
        discount=Decimal(discount),
        total=Decimal(total)
    )
    transaction_item.transaction_item_id = transaction_item_id
    return transaction_item.update()

@eel.expose
def delete_transaction_item(transaction_item_id: int):
    transaction_item = TransactionItem(
        transaction_id=0, 
        product_id=0, 
        quantity=0, 
        price=Decimal(0), 
        discount=Decimal(0), 
        total=Decimal(0) 
    )
    transaction_item.transaction_item_id = transaction_item_id
    return transaction_item.delete()

@eel.expose
def get_transaction_item_by_id(transaction_item_id: int):
    transaction_item = TransactionItem(
        transaction_id=0, 
        product_id=0, 
        quantity=0, 
        price=Decimal(0), 
        discount=Decimal(0), 
        total=Decimal(0) 
    )
    return transaction_item.get_by_id(transaction_item_id)

@eel.expose
def get_all_transaction_items_by_transaction_id(transaction_id: int):
    transaction_item = TransactionItem(
        transaction_id=transaction_id,
        product_id=0, 
        quantity=0, 
        price=Decimal(0), 
        discount=Decimal(0), 
        total=Decimal(0) 
    )
    return transaction_item.get_all_by_transaction_id(transaction_id)
