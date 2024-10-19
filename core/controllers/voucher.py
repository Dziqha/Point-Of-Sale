from datetime import datetime
from decimal import Decimal
import eel
from core.services.voucher import Voucher

@eel.expose
def create_voucher(code: str, discount_value: float, expiration_date: str):
    """Create a new voucher and save to the database."""
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date)
    return voucher.create()

@eel.expose
def update_voucher(voucher_id: int, code: str, discount_value: float, expiration_date: str):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date)
    voucher.voucher_id = voucher_id
    return voucher.update()

@eel.expose
def delete_voucher(voucher_id: int):
    voucher = Voucher(code="")
    voucher.voucher_id = voucher_id
    voucher.delete()
    return f"Voucher with ID {voucher_id} deleted."

@eel.expose
def get_voucher_by_id(voucher_id: int):
    voucher = Voucher(code="")
    return voucher.get_by_id(voucher_id)

@eel.expose
def get_all_vouchers():
    voucher = Voucher(code="")
    return voucher.get_all()
