from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List, Union

from pydantic import BaseModel

from .schemas import User, UserRegistration, UserLogin, UserCreateUpdateSchema, UserPartialUpdateSchema
from .services import UserService
from ..service.constants import ERROR_USER_NOT_FOUND

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ErrorResponse(BaseModel):
    """
    Модель для представления ошибки.

    Attributes:
    - message (str): Сообщение об ошибке.
    """
    message: str


@router.post("/register", response_model=UserRegistration, summary="Register a new user.")
async def register(user_data: UserRegistration) -> User:
    """
    Зарегистрировать нового пользователя.

    Parameters:
    - user_data (UserRegistration): Данные для регистрации нового пользователя.

    Returns:
    - User: Зарегистрированный пользователь.
    """
    user = await UserService.register_user(user_data)
    return user


@router.post("/login", response_model=UserLogin, summary="Authenticate user.")
async def login(login_data: UserLogin) -> Union[User, ErrorResponse]:
    """
    Аутентификация пользователя.

    Parameters:
    - login_data (UserLogin): Данные для аутентификации пользователя.

    Returns:
    - Union[User, ErrorResponse]: Аутентифицированный пользователь или сообщение об ошибке.
    """
    try:
        user = await UserService.authenticate_user(login_data)
        return user
    except ValueError as e:
        return ErrorResponse(message=str(e))


@router.get("/users", response_model=List[User], summary="Get a list of all users.")
async def get_users() -> List[User]:
    """
    Получить список всех пользователей.

    Returns:
    - List[User]: Список всех пользователей.
    """
    users = await User.all()
    return users


@router.get("/users/{user_id}", response_model=User, summary="Get user by ID.")
async def get_user(user_id: int) -> Union[User, HTTPException]:
    """
    Получить пользователя по ID.

    Parameters:
    - user_id (int): ID пользователя для получения.

    Returns:
    - Union[User, HTTPException]: Пользователь с указанным ID или сообщение об ошибке.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail=ErrorResponse(message=ERROR_USER_NOT_FOUND))


@router.put("/users/{user_id}", response_model=UserPartialUpdateSchema, summary="Update user by ID.")
async def update_user(user_id: int, user_data: UserRegistration) -> Union[User, HTTPException]:
    """
    Обновить пользователя по ID.

    Parameters:
    - user_id (int): ID пользователя для обновления.
    - user_data (UserRegistration): Данные для обновления пользователя.

    Returns:
    - Union[User, HTTPException]: Обновленный пользователь или сообщение об ошибке.

    Raises:
    - HTTPException: Если пользователь с указанным ID не найден.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        user.name = user_data.name
        user.email = user_data.email
        user.phone = user_data.phone
        await user.save()
        return user
    else:
        raise HTTPException(status_code=404, detail=ErrorResponse(message=ERROR_USER_NOT_FOUND))


@router.delete("/users/{user_id}", response_model=dict, summary="Delete user by ID.")
async def delete_user(user_id: int) -> dict:
    """
    Удалить пользователя по ID.

    Parameters:
    - user_id (int): ID пользователя для удаления.

    Returns:
    - dict: Сообщение об успешном удалении.

    Raises:
    - HTTPException: Если пользователь с указанным ID не найден.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=ErrorResponse(message=ERROR_USER_NOT_FOUND))
