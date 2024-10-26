import eel
from core.services.category import Category

@eel.expose
def create_category(name: str, description: str = ""):
    category = Category(name=name, description=description)
    response = category.create()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def get_all_categories():
    category = Category('', '')
    response = category.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "category_id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "created_at": row[3]
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
def get_category_by_id(category_id: int):
    category = Category('', '')
    response = category.get_by_id(category_id)

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def update_category(category_id: int, name: str, description: str):
    category = Category(name=name, description=description)
    category.category_id = category_id
    response = category.update()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def delete_category(category_id: int):
    category = Category('', '')
    category.category_id = category_id
    response = category.delete()

    return {
        "status": response["status"],
        "message": response["message"]
    }
