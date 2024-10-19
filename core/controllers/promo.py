import eel
from datetime import datetime
from decimal import Decimal
from core.services.promo import Promo

@eel.expose
def create_promo(name: str, description: str, discount_percentage: float, start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date)
    promo_id = promo.create() 
    return {
        "promo_id": promo_id,
        "name": name,
        "description": description,
        "discount_percentage": str(discount_percentage),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }

@eel.expose
def update_promo(promo_id: int, name: str, description: str, discount_percentage: float, start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date)
    promo.promo_id = promo_id
    promo.update()
    return {
        "promo_id": promo_id,
        "name": name,
        "description": description,
        "discount_percentage": str(discount_percentage),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }

@eel.expose
def delete_promo(promo_id: int):
    promo = Promo(name="")
    promo.promo_id = promo_id
    promo.delete() 
    return f"Promo with ID {promo_id} deleted."

@eel.expose
def get_promo_by_id(promo_id: int):
    promo = Promo(name="")
    promo_data = promo.get_by_id(promo_id)
    if promo_data:
        return {
            "promo_id": promo_data.promo_id,
            "name": promo_data.name,
            "description": promo_data.description,
            "discount_percentage": str(promo_data.discount_percentage),
            "start_date": promo_data.start_date.strftime("%Y-%m-%d"),
            "end_date": promo_data.end_date.strftime("%Y-%m-%d")
        }
    return {"status": "failed", "message": "Promo not found."}

@eel.expose
def get_all_promos():
    promo = Promo(name="")
    promos_data = promo.get_all()
    return [
        {
            "promo_id": p.promo_id,
            "name": p.name,
            "description": p.description,
            "discount_percentage": str(p.discount_percentage),
            "start_date": p.start_date.strftime("%Y-%m-%d"),
            "end_date": p.end_date.strftime("%Y-%m-%d")
        } for p in promos_data
    ]
