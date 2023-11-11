from tortoise.exceptions import IntegrityError
from passlib.hash import bcrypt
from typing import Union
import re

from .models import User, UserRegistration, UserLogin


class UserService:
    @staticmethod
    async def register_user(user_data: UserRegistration) -> User:
        """
        Регистрирует нового пользователя в базе данных.

        Parameters:
        - user_data (UserRegistration): Данные нового пользователя.

        Returns:
        - User: Созданный пользователь.

        Raises:
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

        hashed_password = bcrypt.hash(user_data.password)
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
    async def authenticate_user(login_data: UserLogin) -> Union[User, None]:
        """
        Проверяет учетные данные пользователя и возвращает пользователя, если они верны.

        Parameters:
        - login_data (UserLogin): Данные для аутентификации пользователя.

        Returns:
        - User: Аутентифицированный пользователь.

        Raises:
        - ValueError: Если учетные данные недействительны.
        """
        user = await User.get_or_none(
            (User.email == login_data.email_or_phone) | (User.phone == login_data.email_or_phone)
        )
        if user and bcrypt.verify(login_data.password, user.password):
            return user
        else:
            raise ValueError("Invalid credentials.")
