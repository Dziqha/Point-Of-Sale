import eel
from datetime import datetime
from decimal import Decimal
from core.services.promo import Promo

@eel.expose
def create_promo(name: str, description: str, discount_percentage: float, start_date: str, end_date: str, product_id: int):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(product_id=product_id, name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date)
    response = promo.create()
    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def update_promo(promo_id: int, name: str, description: str, discount_percentage: float, start_date: str, end_date: str, product_id: int):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date, product_id=product_id)
    promo.promo_id = promo_id
    response = promo.update()
    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def delete_promo(promo_id: int):
    promo = Promo()
    promo.promo_id = promo_id
    response = promo.delete()
    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def get_promo_by_id(promo_id: int):
    promo = Promo()
    response = promo.get_by_id(promo_id)

    if response["status"] == "success" and "data" in response:
        promo_data = response["data"]
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "promo_id": promo_data[0],
                "product_id": promo_data[1],
                "name": promo_data[2],
                "description": promo_data[3],
                "discount_percentage": str(promo_data[4]),
                "start_date": promo_data[5],
                "end_date": promo_data[6],
                "product_name": promo_data[7]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
def get_all_promos():
    promo = Promo()
    response = promo.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "promo_id": row[0],
                    "product_id": row[1],
                    "name": row[2],
                    "description": row[3],
                    "discount_percentage": str(row[4]),
                    "start_date": row[5],
                    "end_date": row[6],
                    "product_name": row[7]
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
def get_active_product_promo(product_id: int):
    promo = Promo()
    response = promo.get_active_product_promo(product_id)

    if response["status"] == "success" and "data" in response:
        promo_data = response["data"]
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "promo_id": promo_data[0],
                "product_id": promo_data[1],
                "name": promo_data[2],
                "description": promo_data[3],
                "discount_percentage": str(promo_data[4]),
                "start_date": promo_data[5],
                "end_date": promo_data[6],
                "product_name": promo_data[7]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
def get_all_promos_by_name(name: str):
    promo = Promo()
    response = promo.get_by_name(name)
    
    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "promo_id": row[0],
                    "product_id": row[1],
                    "name": row[2],
                    "description": row[3],
                    "discount_percentage": str(row[4]),
                    "start_date": row[5],
                    "end_date": row[6],
                    "product_name": row[7]
                }
                for row in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }