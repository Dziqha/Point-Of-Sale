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
    transaction_item_id = transaction_item.create()
    return {
        "transaction_item_id": transaction_item_id,
        "transaction_id": transaction_id,
        "product_id": product_id,
        "quantity": quantity,
        "price": str(price),
        "discount": str(discount),
        "total": str(total)
    }

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
    transaction_item.update()
    return {
        "transaction_item_id": transaction_item_id,
        "product_id": product_id,
        "quantity": quantity,
        "price": str(price),
        "discount": str(discount),
        "total": str(total)
    }

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
    transaction_item.delete()
    return f"Transaction item with ID {transaction_item_id} deleted."

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
    transaction_data = transaction_item.get_by_id(transaction_item_id)
    if transaction_data:
        return {
            "transaction_item_id": transaction_data.transaction_item_id,
            "transaction_id": transaction_data.transaction_id,
            "product_id": transaction_data.product_id,
            "quantity": transaction_data.quantity,
            "price": str(transaction_data.price),
            "discount": str(transaction_data.discount),
            "total": str(transaction_data.total)
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
            "transaction_item_id": ti.transaction_item_id,
            "transaction_id": ti.transaction_id,
            "product_id": ti.product_id,
            "quantity": ti.quantity,
            "price": str(ti.price),
            "discount": str(ti.discount),
            "total": str(ti.total)
        } for ti in transaction_items_data
    ]
