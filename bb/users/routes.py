from fastapi import APIRouter, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer

from typing import List

from .models import User, UserRegistration, UserLogin
from .services import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=User, summary="Register a new user.")
async def register(user_data: UserRegistration):
    """
    Register a new user.

    Parameters:
    - user_data (UserRegistration): Data for registering a new user.

    Returns:
    - User: Registered user.
    """
    user = await UserService.register_user(user_data)
    return user


@router.post("/login", response_model=User, summary="Authenticate user.")
async def login(login_data: UserLogin):
    """
    Authenticate a user.

    Parameters:
    - login_data (UserLogin): Data for user authentication.

    Returns:
    - User: Authenticated user.
    """
    user = await UserService.authenticate_user(login_data)
    return user


@router.get("/users", response_model=List[User], summary="Get a list of all users.")
async def get_users():
    """
    Get a list of all users.

    Returns:
    - List[User]: List of all users.
    """
    users = await User.all()
    return users


@router.get("/users/{user_id}", response_model=User, summary="Get user by ID.")
async def get_user(user_id: int):
    """
    Get user by ID.

    Parameters:
    - user_id (int): ID of the user to retrieve.

    Returns:
    - User: User with the specified ID.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", response_model=User, summary="Update user by ID.")
async def update_user(user_id: int, user_data: UserRegistration):
    """
    Update user by ID.

    Parameters:
    - user_id (int): ID of the user to update.
    - user_data (UserRegistration): Data for updating the user.

    Returns:
    - User: Updated user.

    Raises:
    - HTTPException: If the user with the specified ID is not found.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        user.name = user_data.name
        user.email = user_data.email
        user.phone = user_data.phone
        await user.save()
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}", response_model=dict, summary="Delete user by ID.")
async def delete_user(user_id: int):
    """
    Delete user by ID.

    Parameters:
    - user_id (int): ID of the user to delete.

    Returns:
    - dict: Message indicating successful deletion.

    Raises:
    - HTTPException: If the user with the specified ID is not found.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
