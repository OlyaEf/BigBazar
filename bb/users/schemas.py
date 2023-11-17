from datetime import datetime
from typing import Optional, ClassVar

from pydantic import BaseModel, EmailStr, Field
from tortoise.contrib.pydantic import pydantic_model_creator


from .models import User

# Схема для чтения данных пользователя
UserRetrieveSchema = pydantic_model_creator(User, name="User")


class UserBase(BaseModel):
    """
    Базовая Pydantic-модель схемы пользователя.

    Атрибуты:
        email (EmailStr): Email пользователя.
        phone (Optional[str]): Телефон пользователя.
    """
    email: EmailStr = Field(..., max_length=255)
    phone: Optional[str] = None


class UserRegistration(UserBase):
    """
    Pydantic-модель схемы для регистрации пользователя.

    Атрибуты:
        password (str): Пароль пользователя.
        confirm_password (str): Подтверждение пароля пользователя.
    """
    name: str
    password: str
    confirm_password: str

    def __setattr__(self, name, value):
        """
        Переопределенный метод для валидации пароля и его подтверждения.

        Параметры:
        - name (str): Имя атрибута.
        - value: Значение атрибута.

        Вызывает:
        - ValueError: Если атрибут - confirm_password, и значение не совпадает с паролем.
        """
        if name == 'confirm_password':
            if 'password' in self.__dict__ and value != self.__dict__['password']:
                raise ValueError("Password and confirmation password do not match")
        super().__setattr__(name, value)

    class Config:
        from_attributes = True

    Config: ClassVar[Config]  # Аннотация, указывающая, что это не поле модели


class UserLogin(UserBase):
    """
    Pydantic-модель схемы для аутентификации пользователя.

    Атрибуты:
        password (str): Пароль пользователя.
    """
    password: str

    class Config:
        from_attributes = True

    Config: ClassVar[Config]  # Аннотация, указывающая, что это не поле модели


class Token(BaseModel):
    """
    Pydantic-модель схемы для токена доступа.

    Атрибуты:
        access_token (str): Токен доступа.
        refresh_token (str): Токен обновления.
        token_type (str): Тип токена.
    """
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True

    Config: ClassVar[Config]  # Аннотация, указывающая, что это не поле модели


class UserPartialUpdateSchema(UserBase):
    """
    Pydantic-модель схемы для частичного обновления пользователя.

    Поля могут быть предоставлены частично, позволяя обновлять только указанные атрибуты пользователя.

    Атрибуты:
        name (Optional[str]): Имя пользователя.
        email (Optional[EmailStr]): Email пользователя.
        phone (Optional[str]): Телефон пользователя.
        password (Optional[str]): Пароль пользователя.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True

    Config: ClassVar[Config]  # Аннотация, указывающая, что это не поле модели
