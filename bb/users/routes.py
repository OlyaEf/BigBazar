from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import List, Union

from pydantic import BaseModel

from .schemas import User, UserRegistration, UserLogin, UserPartialUpdateSchema, Token, UserRetrieveSchema
from .services import UserService
from ..service.constants import ERROR_USER_NOT_FOUND

users_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ErrorResponse(BaseModel):
    """
    Модель для представления ошибки.

    Атрибуты:
    - message (str): Сообщение об ошибке.
    """
    message: str


@users_router.post("/users/register", response_model=UserRetrieveSchema, summary="Register a new user.")
async def register(user_data: UserRegistration) -> UserRetrieveSchema:
    """
    Зарегистрировать нового пользователя и возвращать зарегистрированные данные.

    Параметры:
        user_data (UserRegistration): Данные для регистрации нового пользователя.

    Возвращает:
        UserRetrieveSchema:: Данные зарегистрированного пользователя.
    """
    user = await UserService.register_user(user_data)
    return user


@users_router.post("/users/login", response_model=Token, summary="Authenticate user.")
async def login(login_data: UserLogin) -> Union[Token, ErrorResponse]:
    """
    Аутентифицировать пользователя и вернуть токен доступа.

    Параметры:
        login_data (UserLogin): Данные для входа пользователя.

    Возвращает:
        Token: Токен доступа, если аутентификация успешна.
        ErrorResponse: Ошибка с сообщением о неверных учетных данных.
    """
    try:
        token = await UserService.authenticate_user(login_data)
        if token:
            return token
        else:
            return ErrorResponse(message="Invalid credentials.")
    except ValueError as e:
        return ErrorResponse(message=str(e))


@users_router.get("/users", response_model=List[UserRetrieveSchema], summary="Get a list of all users.")
async def get_users() -> List[UserRetrieveSchema]:
    """
    Получить список всех пользователей.

    Возвращает:
    - List[User]: Список всех пользователей.
    """
    users = await User.all()
    return [UserRetrieveSchema.from_orm(user) for user in users]


@users_router.get("/users/{user_id}", response_model=UserRetrieveSchema, summary="Get user by ID.")
async def get_user(user_id: int) -> Union[UserRetrieveSchema, HTTPException]:
    """
    Получить данные пользователя по его ID.

    Параметры:
        user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
        UserRetrieveSchema: Данные пользователя, если он найден.
        HTTPException: Исключение с HTTP статусом 404, если пользователь не найден.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        return UserRetrieveSchema.from_orm(user)
    else:
        raise HTTPException(status_code=404, detail={"message": ERROR_USER_NOT_FOUND})


@users_router.put("/users/{user_id}", response_model=UserRetrieveSchema, summary="Update user by ID.")
async def update_user(user_id: int, user_data: UserPartialUpdateSchema) -> Union[UserRetrieveSchema, HTTPException]:
    """
    Обновить данные пользователя по ID. Позволяет частичное или полное обновление.

    Параметры:
        - user_id (int): ID пользователя для обновления.
        - user_data (UserPartialUpdateSchema): Данные для обновления пользователя.

    Возвращает:
        UserRetrieveSchema: Обновленные данные пользователя.
        HTTPException: Исключение с HTTP статусом 404, если пользователь не найден.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        # Обновление только предоставленных полей
        user_data_dict = user_data.model_dump(exclude_unset=True)
        for key, value in user_data_dict.items():
            setattr(user, key, value)
        await user.save()
        return UserRetrieveSchema.from_orm(user)
    else:
        raise HTTPException(status_code=404, detail={"message": ERROR_USER_NOT_FOUND})


@users_router.delete("/users/{user_id}", response_model=dict, summary="Delete user by ID.")
async def delete_user(user_id: int) -> dict:
    """
    Удалить пользователя по ID.

    Параметры:
    - user_id (int): ID пользователя для удаления.

    Возвращает:
    - dict: Сообщение об успешном удалении.

    Вызывает:
    - HTTPException: Если пользователь с указанным ID не найден.
    """
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=ErrorResponse(message=ERROR_USER_NOT_FOUND))


@users_router.get("/users/protected-resource", response_model=dict, summary="Access protected resource.")
async def get_protected_resource(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Получить доступ к защищенному ресурсу с использованием токена.

    Параметры:
    - token (str): Bearer токен для аутентификации.

    Возвращает:
    - dict: Результат защищенного ресурса.
    """
    # Ваш код для доступа к защищенному ресурсу
    result = {"message": "Access to protected resource granted"}
    return result
