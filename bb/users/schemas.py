from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User

# Схема для чтения данных пользователя
UserRetrieveSchema = pydantic_model_creator(User, name="User")


class UserBase(BaseModel):
    """
    Базовая модель пользователя для схемы.

    Attributes:
    - name (str): Имя пользователя (максимальная длина 150 символов).
    - email (EmailStr): Email пользователя (максимальная длина 255 символов).
    - phone (str): Телефон пользователя.
    """
    name: str = Field(..., max_length=150)
    email: EmailStr = Field(..., max_length=255)
    phone: str


class UserRegistration(UserBase):
    """
    Модель для регистрации пользователя.

    Attributes:
    - password (str): Пароль пользователя.
    """
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    """
    Модель для авторизации пользователя.

    Attributes:
    - email_or_phone (str): Email или телефон пользователя.
    - password (str): Пароль пользователя.
    """
    email_or_phone: str
    password: str


class User(UserBase):
    """
    Модель пользователя.

    Attributes:
    - id (Optional[int]): Идентификатор пользователя.
    - created_at (datetime): Дата и время создания пользователя.
    - updated_at (datetime): Дата и время последнего обновления пользователя.
    """
    id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserCreateUpdateSchema(UserBase):
    """
    Модель для создания или обновления пользователя.

    Attributes:
    - name (Optional[str]): Имя пользователя (опционально).
    - email (Optional[str]): Email пользователя (опционально).
    - password (Optional[str]): Пароль пользователя (опционально).
    """
    password: str


class UserPartialUpdateSchema(UserBase):
    """
    Модель для частичного обновления пользователя.

    Attributes:
    - name (Optional[str]): Имя пользователя (опционально).
    - email (Optional[str]): Email пользователя (опционально).
    - password (Optional[str]): Пароль пользователя (опционально).
    """
    password: str
