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
    result = transaction_item.create()
    return result

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
    result = transaction_item.update()
    return result

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
    result = transaction_item.delete()
    return result

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
    transaction_item_data = transaction_item.get_by_id(transaction_item_id)
    if transaction_item_data:
        return {
            "transaction_item_id": transaction_item_data[0],
            "transaction_id": transaction_item_data[1],
            "product_id": transaction_item_data[2],
            "quantity": transaction_item_data[3],
            "price": str(transaction_item_data[4]),
            "discount": str(transaction_item_data[5]),
            "total": str(transaction_item_data[6])
        }
    return {"status": "failed", "message": "Transaction item not found."}

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
    transaction_items_data = transaction_item.get_all_by_transaction_id(transaction_id)
    return [
        {
            "transaction_item_id": ti[0],
            "transaction_id": ti[1],
            "product_id": ti[2],
            "quantity": ti[3],
            "price": str(ti[4]),
            "discount": str(ti[5]),
            "total": str(ti[6])
        } for ti in transaction_items_data
    ]