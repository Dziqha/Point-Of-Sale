import eel
from typing import Optional
from core.services.transaction import Transaction
from core.middlewares.auth import auth_required, AuthLevel

@eel.expose
@auth_required(AuthLevel.CASHIER)
def create_transaction(user_id: int, customer_id: int, paid_amount: float, voucher_id: Optional[int] = None):
    transaction = Transaction(
        user_id=user_id,
        customer_id=customer_id,
        paid_amount=paid_amount,
        voucher_id=voucher_id
    )
    response = transaction.create()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def update_transaction(transaction_id: int, paid_amount: float, voucher_id: Optional[int] = None):
    transaction = Transaction(
        user_id=0,
        customer_id=0,
        paid_amount=paid_amount,
        voucher_id=voucher_id
    )
    transaction.transaction_id = transaction_id
    response = transaction.update()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def delete_transaction(transaction_id: int):
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        paid_amount=0
    )
    transaction.transaction_id = transaction_id
    response = transaction.delete()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
@auth_required(AuthLevel.CASHIER)
def get_transaction_by_id(transaction_id: int):
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        paid_amount=0
    )
    response = transaction.get_by_id(transaction_id)

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "transaction_id": response["data"][0],
                "user_id": response["data"][1],
                "customer_id": response["data"][2],
                "paid_amount": str(response["data"][3]),
                "voucher_id": response["data"][4],
                "created_at": str(response["data"][5]),
                "cashier_name": response["data"][6],
                "customer_phone": response["data"][7]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_all_transactions():
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        paid_amount=0
    )
    response = transaction.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "transaction_id": row[0],
                    "user_id": row[1],
                    "customer_id": row[2],
                    "paid_amount": str(row[3]),
                    "voucher_id": row[4],
                    "created_at": str(row[5]),
                    "cashier_name": row[6],
                    "customer_phone": row[7]
                } for row in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_transactions_by_customer(customer_id: int):
    transaction = Transaction(
        user_id=0,
        customer_id=customer_id, 
        paid_amount=0
    )
    response = transaction.get_by_customer(customer_id)

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "transaction_id": row[0],
                    "user_id": row[1],
                    "customer_id": row[2],
                    "paid_amount": str(row[3]),
                    "voucher_id": row[4],
                    "created_at": str(row[5]),
                    "cashier_name": row[6],
                    "customer_phone": row[7]
                } for row in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_transaction_stats():
    transaction = Transaction(
        user_id=0,
        customer_id=0, 
        paid_amount=0
    )
    response = transaction.get_stats()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }