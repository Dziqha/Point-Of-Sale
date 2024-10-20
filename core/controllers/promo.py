import eel
from datetime import datetime
from decimal import Decimal
from core.services.promo import Promo

@eel.expose
def create_promo(name: str, description: str, discount_percentage: float, start_date: str, end_date: str, product_id: int):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(product_id=product_id, name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date)
    return promo.create()

@eel.expose
def update_promo(promo_id: int, name: str, description: str, discount_percentage: float, start_date: str, end_date: str, product_id: int):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date, product_id=product_id)
    promo.promo_id = promo_id
    return promo.update()

@eel.expose
def delete_promo(promo_id: int):
    promo = Promo()
    promo.promo_id = promo_id
    return promo.delete()

@eel.expose
def get_promo_by_id(promo_id: int):
    promo = Promo()
    promo_data = promo.get_by_id(promo_id)

    if promo_data is None:
        return "Promo not found"
    
    return {
        "promo_id": promo_data[0],
        "product_id": promo_data[1],
        "name": promo_data[2],
        "description": promo_data[3],
        "discount_percentage": str(promo_data[4]),
        "start_date": promo_data[5],
        "end_date": promo_data[6],
        "product_name": promo_data[7]
    }

@eel.expose
def get_all_promos():
    promo = Promo()
    promos_data = promo.get_all()
    return [
        {
            "promo_id": p[0],
            "product_id": p[1],
            "name": p[2],
            "description": p[3],
            "discount_percentage": str(p[4]),
            "start_date": p[5],
            "end_date": p[6],
            "product_name": p[7]
        } for p in promos_data
    ]

@eel.expose
def get_active_product_promo(product_id: int):
    promo = Promo()
    active_promo_data = promo.get_active_product_promo(product_id)

    if active_promo_data is None:
        return "No active promotion found for this product."
    
    return {
        "promo_id": active_promo_data[0],
        "product_id": active_promo_data[1],
        "name": active_promo_data[2],
        "description": active_promo_data[3],
        "discount_percentage": str(active_promo_data[4]),
        "start_date": active_promo_data[5],
        "end_date": active_promo_data[6],
    }