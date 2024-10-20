import eel
from core.services.stock_movement import StockMovement

@eel.expose
def create_stock_movement(product_id: int, user_id: int, movement_type: str, quantity_change: int, reason: str = ""):
    movement = StockMovement(product_id=product_id, user_id=user_id, movement_type=movement_type, quantity_change=quantity_change, reason=reason)
    return movement.create()

@eel.expose
def get_all_stock_movements():
    movement = StockMovement(0, 0, '', 0)
    movements = movement.get_all()
    return [
        {
            "movement_id": m[0],
            "product_id": m[1],
            "user_id": m[2],
            "movement_type": m[3],
            "quantity_change": m[4],
            "reason": m[5],
            "created_at": m[6],
            "product_name": m[7],
            "sku": m[8] if m[8] is not None else "",
            "admin_username": m[9]
        } for m in movements
    ]

@eel.expose
def get_stock_movement_by_id(movement_id: int):
    movement = StockMovement(0, 0, '', 0)
    m = movement.get_by_id(movement_id)
    
    if m is None:
        return "Stock movement not found"
    
    return {
        "movement_id": m[0],
        "product_id": m[1],
        "user_id": m[2],
        "movement_type": m[3],
        "quantity_change": m[4],
        "reason": m[5],
        "created_at": m[6],
        "product_name": m[7],
        "sku": m[8] if m[8] is not None else "",
        "admin_username": m[9]
    }

@eel.expose
def get_stock_movements_by_product_id(product_id: int):
    movement = StockMovement(0, 0, '', 0)
    movements = movement.get_by_product_id(product_id)
    return [
        {
            "movement_id": m[0],
            "product_id": m[1],
            "user_id": m[2],
            "movement_type": m[3],
            "quantity_change": m[4],
            "reason": m[5],
            "created_at": m[6],
            "product_name": m[7],
            "sku": m[8] if m[8] is not None else "",
            "admin_username": m[9]
        } for m in movements
    ]
