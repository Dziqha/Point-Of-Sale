import eel
from core.services.stock_movement import StockMovement

@eel.expose
def create_stock_movement(product_id: int, user_id: int, movement_type: str, quantity_change: int, reason: str = ""):
    movement = StockMovement(product_id=product_id, user_id=user_id, movement_type=movement_type, quantity_change=quantity_change, reason=reason)
    return movement.create()

@eel.expose
def get_all_stock_movements():
    movement = StockMovement(0, 0, '', 0)
    return movement.get_all()

@eel.expose
def get_stock_movement_by_id(movement_id: int):
    movement = StockMovement(0, 0, '', 0)
    return movement.get_by_id(movement_id)

@eel.expose
def update_stock_movement(movement_id: int, product_id: int, user_id: int, movement_type: str, quantity_change: int, reason: str = ""):
    movement = StockMovement(product_id=product_id, user_id=user_id, movement_type=movement_type, quantity_change=quantity_change, reason=reason)
    movement.movement_id = movement_id
    return movement.update()

@eel.expose
def delete_stock_movement(movement_id: int):
    movement = StockMovement(0, 0, '', 0)
    movement.movement_id = movement_id
    return movement.delete()

@eel.expose
def get_stock_movements_by_product_id(product_id: int):
    movement = StockMovement(0, 0, '', 0)
    return movement.get_by_product_id(product_id)
