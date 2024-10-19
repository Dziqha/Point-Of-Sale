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
    return transaction.create()

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
    return transaction.update()

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
    return transaction.delete()

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
    return transaction.get_by_id(transaction_id)

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
    return transaction.get_all()

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
    return transaction.get_by_user_id(user_id)
