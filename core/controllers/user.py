import eel
from core.services.user import User
from core.lib.hash import hash_password, verify_password
from core.middlewares.auth import auth_required, AuthLevel

@eel.expose
@auth_required(AuthLevel.ADMIN)
def create_user(username: str, password: str, role: str):
    user = User(username=username, password=hash_password(password), role=role)
    response = user.create()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
@auth_required(AuthLevel.SUPERUSER)
def get_all_users():
    user = User('', '', '')
    response = user.get_all()

    if response["status"] == "success" and "data" in response:
        return {
            "status": response["status"],
            "message": response["message"],
            "data": [
                {
                    "id": row[0],
                    "username": row[1],
                    "role": row[3],
                    "created_at": row[4]
                }
                for row in response["data"]
            ]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_user_by_id(user_id: int):
    user = User('', '', '')
    response = user.get_by_id(user_id)

    if response["status"] == "success" and "data" in response:
        user_data = response["data"]
        return {
            "id": user_data[0],
            "username": user_data[1],
            "password": user_data[2],
            "role": user_data[3],
            "created_at": user_data[4]
        }
    else:
        return {
            "status": response["status"],
            "message": response["message"]
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def update_user(user_id: int, password: str):
    user_data = get_user_by_id(user_id)
    
    if not user_data or not isinstance(user_data, dict):
        return {
            "status": "error",
            "message": "User not found"
        }

    user = User(
        username=user_data['username'], 
        password=hash_password(password), 
        role=user_data['role']
    )
    user.user_id = user_id
    result = user.update()
    
    if isinstance(result, dict) and result.get('status') == 'success':
        return {
            "status": "success",
            "message": "User password updated successfully"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to update user password"
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def delete_user(user_id: int):
    user = User('', '', '')
    user.user_id = user_id
    response = user.delete()

    return {
        "status": response["status"],
        "message": response["message"]
    }

@eel.expose
def login(username: str, password: str):
    user = User(username=username, password=password, role='')
    token = user.login(username, password)

    if token["status"] == "success":
        return {
            "status": "success",
            "message": "Login successful.",
            "token": token["token"]
        }
    else:
        return {
            "status": "error",
            "message": "Invalid username or password."
        }

@eel.expose
def get_current_session(token: str):
    user = User('', '', '')
    response = user.get_current_session(token)

    return {
        "status": response["status"],
        "message": response["message"],
        "data": response.get("data")
    }

@eel.expose
@auth_required(AuthLevel.CASHIER)
def change_password(token: str, old_password: str, new_password: str):
    user = User('', '', '')
    session_data = user.get_current_session(token)
    
    if isinstance(session_data, dict) and 'error' not in session_data:
        user_id = session_data['data']['user_id']
        response = user.get_by_id(user_id)
        
        if response["status"] == "success" and response["data"]:
            user_data = response["data"]
            
            if verify_password(user_data[2], old_password):
                user = User(
                    username=user_data[1], 
                    password=hash_password(new_password), 
                    role=user_data[3]
                )
                user.user_id = user_id
                update_response = user.update()
                
                if update_response["status"] == "success":
                    return {
                        "status": "success",
                        "message": "Password changed successfully"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Failed to update password"
                    }
            else:
                return {
                    "status": "error",
                    "message": "Incorrect old password"
                }
        else:
            return {
                "status": "error",
                "message": "User not found"
            }
    else:
        return {
            "status": "error",
            "message": "Invalid session"
        }

@eel.expose
@auth_required(AuthLevel.ADMIN)
def get_user_by_role(role: str):
    try:
        user = User('', '', '')
        users_data = user.get_by_role(role)
        
        if not users_data:
            return {
                "status": "error",
                "message": f"No users found with role '{role}'",
            }

        return {
            "status": "success",
            "message": f"Successfully retrieved users with role '{role}'",
            "data": [
                {
                    "id": user[0],
                    "username": user[1],
                    "role": user[3]
                }
                for user in users_data["data"]
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve users: {str(e)}",
            "data": []
        }