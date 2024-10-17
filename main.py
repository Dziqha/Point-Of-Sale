# main.py
import eel
from db import init_db, add_product, get_products

# Initialize the database
init_db()

# Initialize Eel
eel.init('web')

@eel.expose
def add_product_eel(name, price, stock, description, category):
    add_product(name, price, stock, description, category)
    return True

@eel.expose
def get_products_eel():
    products = get_products()
    print("Current products in database:", products)
    return products

def main():
    # Start the web app
    eel.start('index.html', size=(800, 600))

if __name__ == "__main__":
    main()
