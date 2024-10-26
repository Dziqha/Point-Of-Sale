import eel
from datetime import datetime
from decimal import Decimal
from core.services.voucher import Voucher

@eel.expose
def create_voucher(code: str, discount_value: float, expiration_date: str, quota: int):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date, quota=quota)
    response = voucher.create()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def update_voucher(voucher_id: int, code: str, discount_value: float, expiration_date: str, quota: int):
    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    voucher = Voucher(code=code, discount_value=Decimal(discount_value), expiration_date=expiration_date, quota=quota)
    voucher.voucher_id = voucher_id
    response = voucher.update()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def delete_voucher(voucher_id: int):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    voucher.voucher_id = voucher_id
    response = voucher.delete()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def get_voucher_by_id(voucher_id: int):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    response = voucher.get_by_id(voucher_id)

    if response["status"] == "success" and "data" in response:
        voucher_data = response["data"]
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "voucher_id": voucher_data[0],
                "code": voucher_data[1],
                "quota": voucher_data[2],
                "discount_value": voucher_data[3],
                "expiration_date": voucher_data[4]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
def get_voucher_by_code(code: str):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    response = voucher.get_by_code(code)

    if response["status"] == "success" and "data" in response:
        voucher_data = response["data"]
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "voucher_id": voucher_data[0],
                "code": voucher_data[1],
                "quota": voucher_data[2],
                "discount_value": voucher_data[3],
                "expiration_date": voucher_data[4]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
def get_all_voucher_by_code(code: str):
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    response = voucher.get_all_by_code(code)

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def get_all_vouchers():
    voucher = Voucher(code="", discount_value=Decimal(0), expiration_date=datetime.now(), quota=0)
    response = voucher.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "voucher_id": v[0],
                    "code": v[1],
                    "quota": v[2],
                    "discount_value": v[3],
                    "expiration_date": v[4]
                } for v in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }
