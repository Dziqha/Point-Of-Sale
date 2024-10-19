import eel
from core.services.product import Product

@eel.expose
def create_product(name: str, sku: str, barcode: str, category_id: int, price: int, description: str = ""):
    product = Product(name=name, sku=sku, barcode=barcode, category_id=category_id, price=price, description=description)
    return product.create()

@eel.expose
def get_all_products():
    product = Product('', '', '', 0, 0)
    return product.get_all()

@eel.expose
def get_product_by_id(product_id: int):
    product = Product('', '', '', 0, 0)
    return product.get_by_id(product_id)

@eel.expose
def update_product(product_id: int, name: str, sku: str, barcode: str, category_id: int, stock: int, price: int, description: str = ""):
    product = Product(name=name, sku=sku, barcode=barcode, category_id=category_id, price=price, description=description)
    product.product_id = product_id
    return product.update()

@eel.expose
def delete_product(product_id: int):
    product = Product('', '', '', 0, 0)
    product.product_id = product_id 
    return product.delete()

@eel.expose
def search_products_by_name(name: str):
    product = Product('', '', '', 0, 0)
    return product.search_by_name(name)

@eel.expose
def search_product_by_barcode(barcode: str):
    product = Product('', '', '', 0, 0)
    return product.search_by_barcode(barcode)
