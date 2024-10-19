import eel, json
from core.services.category import Category

@eel.expose
def create_category(name: str, description: str = ""):
    category = Category(name=name, description=description)
    return category.create()

@eel.expose
def get_all_categories():
    category = Category('', '')
    rows = category.get_all()

    return [
        {
            "category_id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

@eel.expose
def get_category_by_id(category_id: int):
    category = Category('', '')
    return category.get_by_id(category_id)

@eel.expose
def update_category(category_id: int, name: str, description: str):
    category = Category(name=name, description=description)
    category.category_id = category_id
    return category.update()

@eel.expose
def delete_category(category_id: int):
    category = Category('', '')
    category.category_id = category_id
    return category.delete()
