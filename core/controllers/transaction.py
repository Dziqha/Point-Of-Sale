import eel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from core.services.transaction import Transaction

@eel.expose
def create_transaction(user_id: int, total: float, discount: float, final_total: float, paid_amount: float, return_amount: float, customer_id: Optional[int] = None, voucher_id: Optional[int] = None):
    transaction = Transaction(
        user_id=user_id,
        customer_id=customer_id,
        total=total,
        discount=discount,
        final_total=final_total,
        paid_amount=paid_amount,
        return_amount=return_amount,
        voucher_id=voucher_id
    )
    result = transaction.create()
    return result

@eel.expose
def update_transaction(transaction_id: int, total: float, discount: float, final_total: float, paid_amount: float, return_amount: float, voucher_id: int = None):
    transaction = Transaction(
        user_id=0,
        customer_id=0,
        total=Decimal(total),
        discount=Decimal(discount),
        final_total=Decimal(final_total),
        paid_amount=Decimal(paid_amount),
        return_amount=Decimal(return_amount),
        voucher_id=voucher_id
    )
    transaction.transaction_id = transaction_id
    result = transaction.update()
    return result

@eel.expose
def delete_transaction(transaction_id: int):
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0)
    )
    transaction.transaction_id = transaction_id
    result = transaction.delete()
    return result

@eel.expose
def get_transaction_by_id(transaction_id: int):
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0)
    )
    transaction_data = transaction.get_by_id(transaction_id)
    if transaction_data:
        return {
            "transaction_id": transaction_data[0],
            "user_id": transaction_data[1],
            "customer_id": transaction_data[2],
            "total": str(transaction_data[3]),
            "discount": str(transaction_data[4]),
            "final_total": str(transaction_data[5]),
            "paid_amount": str(transaction_data[6]),
            "return_amount": str(transaction_data[7]),
            "voucher_id": transaction_data[8],
            "created_at": str(transaction_data[9]),
            "cashier_name": transaction_data[10],
            "customer_phone": transaction_data[11]
        }
    return {"status": "failed", "message": "Transaction not found."}

@eel.expose
def get_all_transactions():
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0)
    )
    transactions_data = transaction.get_all()
    return [
        {
            "transaction_id": t[0],
            "user_id": t[1],
            "customer_id": t[2],
            "total": str(t[3]),
            "discount": str(t[4]),
            "final_total": str(t[5]),
            "paid_amount": str(t[6]),
            "return_amount": str(t[7]),
            "voucher_id": t[8],
            "created_at": str(t[9]),
            "cashier_name": t[10],
            "customer_phone": t[11]
        } for t in transactions_data
    ]

@eel.expose
def get_transactions_by_user_id(user_id: int):
    transaction = Transaction(
        user_id=user_id,
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0)
    )
    transactions_data = transaction.get_by_user_id(user_id)
    return [
        {
            "transaction_id": t[0],
            "user_id": t[1],
            "customer_id": t[2],
            "total": str(t[3]),
            "discount": str(t[4]),
            "final_total": str(t[5]),
            "paid_amount": str(t[6]),
            "return_amount": str(t[7]),
            "voucher_id": t[8],
            "created_at": str(t[9])
        } for t in transactions_data
    ]

@eel.expose
def get_transaction_stats():
    transaction = Transaction(
        user_id=0,
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0)
    )
    stats = transaction.get_stats()

    # Extract the first element of the outer array
    if stats and isinstance(stats[0], (list, tuple)):
        stats = stats[0]  # Unwrap the inner list

    return {
        "daily_new_transactions": stats[0],
        "weekly_new_transactions": stats[1],
        "monthly_new_transactions": stats[2],
    }
