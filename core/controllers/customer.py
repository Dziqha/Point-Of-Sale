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
    customer.delete()
    return f"Customer with ID {customer_id} deleted."

@eel.expose
def get_customer_by_id(customer_id: int):
    customer = Customer(name="")
    customer_data = customer.get_by_id(customer_id)
    if customer_data:
        return {
            "customer_id": customer_data[0],
            "name": customer_data[1],
            "email": customer_data[2],
            "phone": customer_data[3],
            "address": customer_data[4]
        }
    return {"status": "failed", "message": "Customer not found."}

@eel.expose
def get_all_customers():
    customer = Customer(name="")
    customers_data = customer.get_all()
    return [
        {
            "customer_id": c[0],
            "name": c[1],
            "email": c[2],
            "phone": c[3],
            "address": c[4]
        } for c in customers_data
    ]
