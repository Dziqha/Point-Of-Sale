import eel
from datetime import datetime
from decimal import Decimal
from core.services.voucher import Voucher

@eel.expose
def create_voucher(code: str, discount_value: float, expiration_date: str, quota: int):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date, quota=quota)
    return voucher.create()
    
@eel.expose
def update_voucher(voucher_id: int, code: str, discount_value: float, expiration_date: str, quota: int):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date, quota=quota)
    voucher.voucher_id = voucher_id
    return voucher.update()

@eel.expose
def delete_voucher(voucher_id: int):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    voucher.voucher_id = voucher_id
    return voucher.delete()

@eel.expose
def get_voucher_by_id(voucher_id: int):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    voucher_data = voucher.get_by_id(voucher_id)
    
    if voucher_data is None:
        return "Voucher not found"
    
    return {
        "voucher_id": voucher_data[0],
        "code": voucher_data[1],
        "discount_value": str(voucher_data[3]),
        "expiration_date": voucher_data[4],
        "quota": voucher_data[2]
    }

@eel.expose
def get_voucher_by_code(code: str):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    voucher_data = voucher.get_by_code(code)
    
    if voucher_data is None:
        return "Voucher not found"
    
    return {
        "voucher_id": voucher_data[0],
        "code": voucher_data[1],
        "discount_value": str(voucher_data[3]),
        "expiration_date": voucher_data[4],
        "quota": voucher_data[2]
    }

@eel.expose
def get_all_vouchers():
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    vouchers_data = voucher.get_all()
    return [
        {
            "voucher_id": v[0],
            "code": v[1],
            "discount_value": str(v[3]),
            "expiration_date": v[4],
            "quota": v[2]
        } for v in vouchers_data
    ]