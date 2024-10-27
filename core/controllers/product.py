import eel
from core.services.product import Product

@eel.expose
def create_product(name: str, sku: str, barcode: str, category_id: int, price: float, description: str = ""):
    product = Product(name=name, sku=sku, barcode=barcode, category_id=category_id, price=price, description=description)
    response = product.create()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def get_all_products():
    product = Product('', '', '', 0, 0)
    response = product.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "product_id": row[0],
                    "name": row[1],
                    "sku": row[2],
                    "barcode": row[3],
                    "category_id": row[4],
                    "stock": row[5],
                    "price": row[6],
                    "description": row[7],
                    "created_at": row[8],
                    "updated_at": row[9],
                    "category_name": row[10]
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
def get_product_by_id(product_id: int):
    product = Product('', '', '', 0, 0)
    response = product.get_by_id(product_id)

    if response["status"] == "success" and "data" in response:
        row = response["data"]
        return {
            "status": response["status"],
            "message": response["message"],
            "data": {
                "product_id": row[0],
                "name": row[1],
                "sku": row[2],
                "barcode": row[3],
                "category_id": row[4],
                "stock": row[5],
                "price": row[6],
                "description": row[7],
                "created_at": row[8],
                "updated_at": row[9],
                "category_name": row[10]
            }
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
def update_product(product_id: int, name: str, sku: str, barcode: str, category_id: int, stock: int, price: float, description: str = ""):
    product = Product(name=name, sku=sku, barcode=barcode, category_id=category_id, price=price, description=description)
    product.product_id = product_id
    product.stock = stock
    response = product.update()

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
def get_out_of_stock():
    product = Product('', '', '', 0, 0)
    response = product.get_out_of_stock()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "product_id": row[0],
                    "name": row[1],
                    "sku": row[2],
                    "barcode": row[3],
                    "category_id": row[4],
                    "stock": row[5],
                    "price": row[6],
                    "description": row[7],
                    "created_at": row[8],
                    "updated_at": row[9],
                    "category_name": row[10]
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
def search_products_by_name(name: str):
    product = Product('', '', '', 0, 0)
    response = product.search_by_name(name)

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "product_id": row[0],
                    "name": row[1],
                    "sku": row[2],
                    "barcode": row[3],
                    "category_id": row[4],
                    "stock": row[5],
                    "price": row[6],
                    "description": row[7],
                    "created_at": row[8],
                    "updated_at": row[9],
                    "category_name": row[10]
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
def search_product_by_barcode(barcode: str):
    product = Product('', '', '', 0, 0)
    response = product.search_by_barcode(barcode)

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "product_id": row[0],
                    "name": row[1],
                    "sku": row[2],
                    "barcode": row[3],
                    "category_id": row[4],
                    "stock": row[5],
                    "price": row[6],
                    "description": row[7],
                    "created_at": row[8],
                    "updated_at": row[9],
                    "category_name": row[10]
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
def delete_product(product_id: int):
    product = Product('', '', '', 0, 0)
    product.product_id = product_id
    response = product.delete()
    
    return {
        "status": response["status"],
        "message": response["message"]
    }

            