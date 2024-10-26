import eel
from core.services.customer import Customer

@eel.expose
def create_customer(name: str, email: str = "", phone: str = "", address: str = ""):
    customer = Customer(name=name, email=email, phone=phone, address=address)
    response = customer.create()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def update_customer(customer_id: int, name: str, email: str = "", phone: str = "", address: str = ""):
    customer = Customer(name=name, email=email, phone=phone, address=address)
    customer.customer_id = customer_id
    response = customer.update()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def delete_customer(customer_id: int):
    customer = Customer(name="")
    customer.customer_id = customer_id
    response = customer.delete()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def get_customer_by_id(customer_id: int):
    customer = Customer(name="")
    response = customer.get_by_id(customer_id)

    return {
        "status": response["status"],
        "message": response["message"],
        "data": {
            "customer_id": response["data"][0],
            "name": response["data"][1],
            "email": response["data"][2],
            "phone": response["data"][3],
            "address": response["data"][4]
        } if response["status"] == "success" and "data" in response else None
    }

@eel.expose
def get_customer_by_phone(customer_phone: str):
    customer = Customer(name="")
    response = customer.get_by_phone(customer_phone)

    return {
        "status": response["status"],
        "message": response["message"],
        "data": {
            "customer_id": response["data"][0],
            "name": response["data"][1],
            "email": response["data"][2],
            "phone": response["data"][3],
            "address": response["data"][4]
        } if response["status"] == "success" and "data" in response else None
    }

@eel.expose
def get_all_customers():
    customer = Customer(name="")
    response = customer.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "customer_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "phone": row[3],
                    "address": row[4]
                } for row in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }
