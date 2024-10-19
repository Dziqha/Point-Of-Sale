from typing import Optional
import eel
from datetime import datetime
from decimal import Decimal
from core.services.transaction import Transaction

@eel.expose
def create_transaction(user_id: int, customer_id: int, total: float, discount: float, final_total: float, paid_amount: float, return_amount: float, voucher_id: Optional[int] = None):
    transaction = Transaction(
        user_id=user_id,
        customer_id=customer_id,
        total=Decimal(total),
        discount=Decimal(discount),
        final_total=Decimal(final_total),
        paid_amount=Decimal(paid_amount),
        return_amount=Decimal(return_amount),
        voucher_id=voucher_id
    )
    transaction_id = transaction.create()
    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "customer_id": customer_id,
        "total": total,
        "discount": discount,
        "final_total": final_total,
        "paid_amount": paid_amount,
        "return_amount": return_amount,
        "voucher_id": voucher_id
    }

@eel.expose
def update_transaction(transaction_id: int, total: float, discount: float, final_total: float, paid_amount: float, return_amount: float, voucher_id: Optional[int] = None):
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
    transaction.update()
    return {
        "transaction_id": transaction_id,
        "total": total,
        "discount": discount,
        "final_total": final_total,
        "paid_amount": paid_amount,
        "return_amount": return_amount,
        "voucher_id": voucher_id
    }

@eel.expose
def delete_transaction(transaction_id: int):
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0), 
        voucher_id=None 
    )
    transaction.transaction_id = transaction_id
    transaction.delete()
    return f"Transaction with ID {transaction_id} deleted."

@eel.expose
def get_transaction_by_id(transaction_id: int):
    transaction = Transaction(
        user_id=0, 
        customer_id=0, 
        total=Decimal(0), 
        discount=Decimal(0), 
        final_total=Decimal(0), 
        paid_amount=Decimal(0), 
        return_amount=Decimal(0), 
        voucher_id=None 
    )
    transaction_data = transaction.get_by_id(transaction_id)
    if transaction_data:
        return {
            "transaction_id": transaction_data.transaction_id,
            "user_id": transaction_data.user_id,
            "customer_id": transaction_data.customer_id,
            "total": str(transaction_data.total),
            "discount": str(transaction_data.discount),
            "final_total": str(transaction_data.final_total),
            "paid_amount": str(transaction_data.paid_amount),
            "return_amount": str(transaction_data.return_amount),
            "voucher_id": transaction_data.voucher_id
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
        return_amount=Decimal(0), 
        voucher_id=None 
    )
    transactions_data = transaction.get_all()
    return [
        {
            "transaction_id": t.transaction_id,
            "user_id": t.user_id,
            "customer_id": t.customer_id,
            "total": str(t.total),
            "discount": str(t.discount),
            "final_total": str(t.final_total),
            "paid_amount": str(t.paid_amount),
            "return_amount": str(t.return_amount),
            "voucher_id": t.voucher_id
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
        return_amount=Decimal(0), 
        voucher_id=None 
    )
    transactions_data = transaction.get_by_user_id(user_id)
    return [
        {
            "transaction_id": t.transaction_id,
            "user_id": t.user_id,
            "customer_id": t.customer_id,
            "total": str(t.total),
            "discount": str(t.discount),
            "final_total": str(t.final_total),
            "paid_amount": str(t.paid_amount),
            "return_amount": str(t.return_amount),
            "voucher_id": t.voucher_id
        } for t in transactions_data
    ]
