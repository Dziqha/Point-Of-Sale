import eel
from core.services.customer import Customer

@eel.expose
def create_customer(name: str, email: str = "", phone: str = "", address: str = ""):
    customer = Customer(name=name, email=email, phone=phone, address=address)
    return customer.create()

@eel.expose
def update_customer(customer_id: int, name: str, email: str = "", phone: str = "", address: str = ""):
    customer = Customer(name=name, email=email, phone=phone, address=address)
    customer.customer_id = customer_id
    return customer.update()

@eel.expose
def delete_customer(customer_id: int):
    customer = Customer(name="")
    customer.customer_id = customer_id
    return customer.delete()

@eel.expose
def get_customer_by_id(customer_id: int):
    customer = Customer(name="")
    return customer.get_by_id(customer_id)

@eel.expose
def get_all_customers():
    customer = Customer(name="")
    return customer.get_all()
