import eel
from core.services.stock_movement import StockMovement
from core.middlewares.auth import auth_required, AuthLevel

@eel.expose
@auth_required(AuthLevel.ADMIN)
def create_stock_movement(product_id: int, user_id: int, movement_type: str, quantity_change: int, reason: str = ""):
    movement = StockMovement(product_id=product_id, user_id=user_id, movement_type=movement_type, quantity_change=quantity_change, reason=reason)
    response = movement.create()
    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_all_stock_movements():
    movement = StockMovement(0, 0, '', 0)
    response = movement.get_all()
    if response['status'] == 'success' and 'data' in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
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
                } for m in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }
@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_stock_movement_by_id(movement_id: int):
    movement = StockMovement(0, 0, '', 0)
    response = movement.get_by_id(movement_id)
    
    if response['status'] == 'success' and 'data' in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "movement_id": response["data"][0],
                "product_id": response["data"][1],
                "user_id": response["data"][2],
                "movement_type": response["data"][3],
                "quantity_change": response["data"][4],
                "reason": response["data"][5],
                "created_at": response["data"][6],
                "product_name": response["data"][7],
                "sku": response["data"][8] if response["data"][8] is not None else "",
                "admin_username": response["data"][9]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_stock_movements_by_product_id(product_id: int):
    movement = StockMovement(0, 0, '', 0)
    response = movement.get_by_product_id(product_id)

    if response['status'] == 'success' and 'data' in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
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
                } for m in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }