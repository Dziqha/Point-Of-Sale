import eel
from typing import Optional
from core.services.cashier import Cashier
from core.middlewares.auth import auth_required, AuthLevel
from core.lib.hash import hash_password

@eel.expose
@auth_required(AuthLevel.ADMIN)
def create_cashier(username: str, password: str):
    cashier = Cashier(username=username, password=hash_password(password))
    response = cashier.create()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_all_cashiers():
    cashier = Cashier(username='', password='')
    response = cashier.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "id": row[0],
                    "username": row[1],
                    "created_at": row[4]
                }
                for row in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_cashier_by_id(cashier_id: int):
    cashier = Cashier(username='', password='')
    response = cashier.get_by_id(cashier_id)

    if response["status"] == "success" and "data" in response:
        cashier_data = response["data"]
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "id": cashier_data[0],
                "username": cashier_data[1],
                "created_at": cashier_data[4]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def update_cashier(cashier_id: int, username: Optional[str] = None, password: Optional[str] = None):
    cashier = Cashier(username='', password='')
    existing_cashier = cashier.get_by_id(cashier_id)
    
    if existing_cashier["status"] != "success":
        return {
            "status": "error",
            "message": "Cashier not found"
        }

    cashier_data = existing_cashier["data"]
    updated_cashier = Cashier(
        username=username if username else cashier_data[1],
        password=hash_password(password) if password else cashier_data[2]
    )
    updated_cashier.user_id = cashier_id
    
    response = updated_cashier.update()
    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def delete_cashier(cashier_id: int):
    cashier = Cashier(username='', password='')
    cashier.user_id = cashier_id
    response = cashier.delete()

    return {
        "status": response["status"],
        "message": response["message"]
    }