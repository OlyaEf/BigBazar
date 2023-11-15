import re
import os
import logging

from tortoise.exceptions import IntegrityError
import bcrypt
from typing import Union
from .models import User
from .schemas import UserLogin, Token, UserRegistration
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))


class UserService:
    @staticmethod
    async def register_user(user_data: UserRegistration) -> User:
        """
        Регистрирует нового пользователя в базе данных.

        Параметры:
        - user_data (UserRegistration): Данные нового пользователя.

        Возвращает:
        - User: Созданный пользователь.

        Вызывает:
        - ValueError:
        Если пользователь с таким email или phone уже существует.
        Если пароль не соответствует условиям.
        Если телефон не соответствует маске.
        """
        # Проверка пароля
        if not re.match(r'^(?=.*[A-Z])(?=.*[$%&!:]).{8,}$', user_data.password):
            raise ValueError("Password must be at least 8 characters, "
                             "contain at least 1 uppercase letter, and include at least 1 special character.")
        # Проверка телефона
        if not re.match(r'^\+7\d{10}$', user_data.phone):
            raise ValueError("Phone must start with +7 and have 10 digits.")

        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            user = await User.create(
                name=user_data.name,
                email=user_data.email,
                phone=user_data.phone,
                password=hashed_password
            )
            return user
        except IntegrityError as e:
            if "email" in str(e):
                raise ValueError("User with this email already exists.")
            elif "phone" in str(e):
                raise ValueError("User with this phone already exists.")
            else:
                raise ValueError("Failed to register user. Reason: " + str(e))

    @staticmethod
    async def authenticate_user(login_data: UserLogin) -> Union[Token, None]:
        """
        Аутентифицирует пользователя.

        Параметры:
            login_data (UserLogin): Данные для входа пользователя.

        Возвращает:
            Token: Токен доступа и обновления, если аутентификация успешна.
            None: Если аутентификация не удалась.
        """
        user = await User.get_or_none(email=login_data.email)
        if user and user.check_password(login_data.password):
            access_token = UserService.create_access_token(data={"sub": user.email}, expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            refresh_token = UserService.create_refresh_token(data={"sub": user.email}, expires_delta=timedelta(
                minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
        else:
            logging.warning(f"Authentication failed for {login_data.email}")
            return None

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """
        Создает аксес токен доступа JWT.

        Параметры:
            data (dict): Данные для включения в токен.
            expires_delta (timedelta, optional): Время жизни токена.

        Возвращает:
            str: Токен доступа JWT.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
        """
        Создает рефреш токен обновления JWT.

        Параметры:
            data (dict): Данные для включения в токен.
            expires_delta (timedelta, optional): Время жизни токена.

        Возвращает:
            str: Токен обновления JWT.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

