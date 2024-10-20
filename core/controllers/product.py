import eel
from core.services.product import Product

@eel.expose
def create_product(name: str, sku: str, barcode: str, category_id: int, price: int, description: str = ""):
    product = Product(name=name, sku=sku, barcode=barcode, category_id=category_id, price=price, description=description)
    result = product.create()
    return result


@eel.expose
def get_all_products():
    product = Product('', '', '', 0, 0)
    products_data = product.get_all()

    return [
        {
            "product_id": p[0],
            "name": p[1],
            "sku": p[2],
            "barcode": p[3],
            "stock": p[4],
            "price": p[5],
            "description": p[6],
            "category_id": p[7],
            "category_name": p[8],
            "created_at": p[9],
            "updated_at": p[10]
        } for p in products_data
    ]


@eel.expose
def get_product_by_id(product_id: int):
    product = Product('', '', '', 0, 0)
    p = product.get_by_id(product_id)

    if p is None:
        return "Product not found"

    return {
        "product_id": p[0],
        "name": p[1],
        "sku": p[2],
        "barcode": p[3],
        "stock": p[4],
        "price": p[5],
        "description": p[6],
        "category_id": p[7],
        "category_name": p[8],
        "created_at": p[9],
        "updated_at": p[10]
    }


@eel.expose
def update_product(product_id: int, name: str, sku: str, barcode: str, category_id: int, stock: int, price: int, description: str = ""):
    product = Product(name=name, sku=sku, barcode=barcode, category_id=category_id, price=price, description=description)
    product.product_id = product_id
    result = product.update()
    return result


@eel.expose
def delete_product(product_id: int):
    product = Product('', '', '', 0, 0)
    product.product_id = product_id
    result = product.delete()
    return result


@eel.expose
def search_products_by_name(name: str):
    product = Product('', '', '', 0, 0)
    products_data = product.search_by_name(name)

    return [
        {
            "product_id": p[0],
            "name": p[1],
            "sku": p[2],
            "barcode": p[3],
            "stock": p[4],
            "price": p[5],
            "description": p[6],
            "category_id": p[7],
            "category_name": p[8],
            "created_at": p[9],
            "updated_at": p[10]
        } for p in products_data
    ]


@eel.expose
def search_product_by_barcode(barcode: str):
    product = Product('', '', '', 0, 0)
    products_data = product.search_by_barcode(barcode)

    return [
        {
            "product_id": p[0],
            "name": p[1],
            "sku": p[2],
            "barcode": p[3],
            "stock": p[4],
            "price": p[5],
            "description": p[6],
            "category_id": p[7],
            "category_name": p[8],
            "created_at": p[9],
            "updated_at": p[10]
        } for p in products_data
    ]