from datetime import datetime
from decimal import Decimal
import eel
from core.services.voucher import Voucher

@eel.expose
def create_voucher(code: str, discount_value: float, expiration_date: str):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date)
    voucher_id = voucher.create()
    return {
        "voucher_id": voucher_id,
        "code": code,
        "discount_value": discount_value,
        "expiration_date": expiration_date.strftime("%Y-%m-%d")
    }

@eel.expose
def update_voucher(voucher_id: int, code: str, discount_value: float, expiration_date: str):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date)
    voucher.voucher_id = voucher_id
    voucher.update()
    return {
        "voucher_id": voucher_id,
        "code": code,
        "discount_value": discount_value,
        "expiration_date": expiration_date.strftime("%Y-%m-%d")
    }

@eel.expose
def delete_voucher(voucher_id: int):
    """Delete a voucher by ID."""
    voucher = Voucher(code="")
    voucher.voucher_id = voucher_id
    voucher.delete()
    return f"Voucher with ID {voucher_id} deleted."

@eel.expose
def get_voucher_by_id(voucher_id: int):
    voucher = Voucher(code="")
    voucher_data = voucher.get_by_id(voucher_id)
    if voucher_data:
        return {
            "voucher_id": voucher_data.voucher_id,
            "code": voucher_data.code,
            "discount_value": str(voucher_data.discount_value),
            "expiration_date": voucher_data.expiration_date.strftime("%Y-%m-%d")
        }
    return {"status": "failed", "message": "Voucher not found."}

@eel.expose
def get_all_vouchers():
    voucher = Voucher(code="")
    vouchers_data = voucher.get_all()
    return [
        {
            "voucher_id": v.voucher_id,
            "code": v.code,
            "discount_value": str(v.discount_value),
            "expiration_date": v.expiration_date.strftime("%Y-%m-%d")
        } for v in vouchers_data
    ]
