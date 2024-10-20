import eel
from core.services.user import User

@eel.expose
def create_user(username: str, password: str, role: str):
    user = User(username=username, password=password, role=role)
    created_user = user.create()

    if isinstance(created_user, User):
        return {
            "id": created_user.user_id,
            "username": created_user.username,
            "role": created_user.role
        }
    
    return created_user 

@eel.expose
def get_all_users():
    user = User('', '', '')
    users = user.get_all()

    return [
        {"id": u[0], "username": u[1], "role": u[3]} 
        for u in users
    ]

@eel.expose
def get_user_by_id(user_id: int):
    user = User('', '', '')
    user_data = user.get_by_id(user_id)

    if user_data:
        return {
            "id": user_data[0],
            "username": user_data[1],
            "password": user_data[2],
            "role": user_data[3]
        }

    return None 
@eel.expose
def get_user_by_role(role: str):
    user = User('', '', '')
    user_data = user.get_by_role(role)

    if user_data:
        
        return [{"id": u[0], "username": u[1]} for u in user_data]
    return [] 

@eel.expose
def update_user(user_id: int, password: str):
    user_data = get_user_by_id(user_id)
    
    if not user_data:
        return {"error": "User not found"}

    user = User(username=user_data['username'], password=password, role=user_data['role'])
    user.user_id = user_data['id'] 
    user.update() 

    return {"message": "User updated successfully!"}

@eel.expose
def delete_user(user_id: int):
    user = User('', '', '')
    user.user_id = user_id
    return user.delete()  

@eel.expose
def login(username: str, password: str):
    user = User(username=username, password=password, role='')
    token = user.login(username, password)
    
    if token:
        return token 
    else:
        return None

@eel.expose
def get_current_session(token: str):
    user = User('', '', '')
    session_data = user.get_current_session(token)

    if isinstance(session_data, dict):
        return {
            "id": session_data.get("user_id"), 
            "username": session_data.get("username"),
            "role": session_data.get("role")
        }

    if session_data:
        return {
            "id": session_data.user_id,
            "username": session_data.username,
            "role": session_data.role
        }

    return None
