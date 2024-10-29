import jwt
import eel
from functools import wraps
from enum import IntEnum

SECRET_KEY = "super_duper_secret_key"
jwt_token = None

class AuthLevel(IntEnum):
    NONE = 0
    CASHIER = 1
    ADMIN = 2
    SUPERUSER = 3

def get_role_level(role: str) -> int:
    role_levels = {
        'cashier': AuthLevel.CASHIER,
        'admin': AuthLevel.ADMIN,
        'superuser': AuthLevel.SUPERUSER
    }
    return role_levels.get(role, 0)

def auth_required(min_level: AuthLevel = AuthLevel.NONE):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if min_level == AuthLevel.NONE:
                return func(*args, **kwargs)

            global jwt_token
            
            if not jwt_token:
                return {
                    "status": "error",
                    "message": "Authentication required."
                }

            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
                user_role = payload.get('role', '')
                user_level = get_role_level(user_role)

                if user_level < min_level:
                    return {
                        "status": "error",
                        "message": "Insufficient privileges."
                    }

                return func(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return {
                    "status": "error",
                    "message": "Token has expired."
                }
            except jwt.InvalidTokenError:
                return {
                    "status": "error",
                    "message": "Invalid token."
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Authentication error: {str(e)}"
                }

        return wrapper
    return decorator

@eel.expose
def set_jwt_token(token):
    global jwt_token
    jwt_token = token

@eel.expose
def get_jwt_token():
    global jwt_token
    return jwt_token

@eel.expose
def reset_jwt_token():
    global jwt_token
    jwt_token = None