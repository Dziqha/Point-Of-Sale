import eel
from core.services.user import User

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