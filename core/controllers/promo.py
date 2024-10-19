import eel
from datetime import datetime
from decimal import Decimal
from core.services.promo import Promo

@eel.expose
def create_promo(name: str, description: str, discount_percentage: float, start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date)
    return promo.create()

@eel.expose
def update_promo(promo_id: int, name: str, description: str, discount_percentage: float, start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    promo = Promo(name=name, description=description, discount_percentage=Decimal(discount_percentage), start_date=start_date, end_date=end_date)
    promo.promo_id = promo_id
    return promo.update()

@eel.expose
def delete_promo(promo_id: int):
    promo = Promo(name="")
    promo.promo_id = promo_id
    return promo.delete()

@eel.expose
def get_promo_by_id(promo_id: int):
    promo = Promo(name="")
    return promo.get_by_id(promo_id)

@eel.expose
def get_all_promos():
    promo = Promo(name="")
    return promo.get_all()
