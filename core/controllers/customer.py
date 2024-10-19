import eel
from core.services.customer import Customer

@eel.expose
def create_customer(name: str, email: str = "", phone: str = "", address: str = ""):
    """Create a new customer and save it to the database."""
    customer = Customer(name=name, email=email, phone=phone, address=address)
    customer_id = customer.create() 
    return {
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address
    }

@eel.expose
def update_customer(customer_id: int, name: str, email: str = "", phone: str = "", address: str = ""):
    customer = Customer(name=name, email=email, phone=phone, address=address)
    customer.customer_id = customer_id
    customer.update()
    return {
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address
    }

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
            "customer_id": customer_data.customer_id,
            "name": customer_data.name,
            "email": customer_data.email,
            "phone": customer_data.phone,
            "address": customer_data.address
        }
    return {"status": "failed", "message": "Customer not found."}

@eel.expose
def get_all_customers():
    customer = Customer(name="")
    customers_data = customer.get_all()
    return [
        {
            "customer_id": c.customer_id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address
        } for c in customers_data
    ]
