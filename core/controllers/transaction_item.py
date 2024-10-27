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
    response = transaction_item.create()
    
    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "transaction_item_id": response["data"]["transaction_item_id"],
                "transaction_id": response["data"]["transaction_id"],
                "product_id": response["data"]["product_id"],
                "quantity": response["data"]["quantity"],
                "price": response["data"]["price"],
                "discount": response["data"]["discount"],
                "total": response["data"]["total"]
            }
        }
    return {
        "status": response["status"],
        "message": response["message"]
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
    response = transaction_item.get_by_id(transaction_item_id)

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "transaction_item_id": response["data"]["transaction_item_id"],
                "transaction_id": response["data"]["transaction_id"],
                "product_id": response["data"]["product_id"],
                "quantity": response["data"]["quantity"],
                "price": response["data"]["price"],
                "discount": response["data"]["discount"],
                "total": response["data"]["total"]
            }
        }
    return {"status": "error", "message": "Transaction item not found."}

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
    response = transaction_item.get_all_by_transaction_id(transaction_id)

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "transaction_item_id": ti["transaction_item_id"],
                    "transaction_id": ti["transaction_id"],
                    "product_id": ti["product_id"],
                    "product_name": ti["product_name"],
                    "product_sku": ti["product_sku"],
                    "quantity": ti["quantity"],
                    "price": ti["price"],
                    "discount": ti["discount"],
                    "total": ti["total"]
                } for ti in response["data"]
            ]
        }
    return {"status": "error", "message": "No transaction items found for the given transaction ID."}