import eel
from core.services.user import User

@eel.expose
def create_user(username: str, password: str, role: str):
    user = User(username=username, password=password, role=role)
    return user.create()

@eel.expose
def get_all_users():
    user = User('', '', '')
    return user.get_all()

@eel.expose
def get_user_by_id(user_id: int):
    user = User('', '', '')
    return user.get_by_id(user_id)

@eel.expose
def update_user(user_id: int, username: str, password: str, role: str):
    user = User(username=username, password=password, role=role)
    user.user_id = user_id
    return user.update()

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
    return session_data
