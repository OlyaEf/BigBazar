from tortoise import fields, models
from pydantic import BaseModel, validator
from passlib.hash import bcrypt


class User(models.Model):
    """
    Модель пользователя.

    Атрибуты:
    - name (str): Имя пользователя (максимальная длина 150 символов).
    - email (str): Email пользователя (уникальный).
    - phone (str): Телефон пользователя (уникальный).
    - password (str): Пароль пользователя.

    Методы:
    - __str__(): Возвращает имя пользователя в виде строки.

    PydanticMeta:
    - exclude (list): Исключает поле пароля из модели Pydantic.
    """
    name = fields.CharField(max_length=150)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=15, unique=True)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class PydanticMeta:
        app = 'models'
        exclude = ['password']

    def __str__(self) -> str:
        """
        Возвращает e-mail пользователя в виде строки.
        """
        return self.email

    @classmethod
    async def create_user(cls, name: str, email: str, phone: str, password: str) -> 'User':
        hashed_password = bcrypt.hash(password)
        return await cls.create(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password
        )


class UserRegistration(BaseModel):
    """
    Модель для регистрации пользователя.

    Атрибуты:
    - name (str): Имя пользователя.
    - email (str): Email пользователя.
    - phone (str): Телефон пользователя.
    - password (str): Пароль пользователя.
    - confirm_password (str): Подтверждение пароля пользователя.

    Методы:
    - __setattr__: Переопределенный метод для валидации пароля и его подтверждения.
    """

    name: str
    email: str
    phone: str
    password: str
    confirm_password: str

    def __setattr__(self, name, value):
        """
        Переопределенный метод для валидации пароля и его подтверждения.

        Parameters:
        - name (str): Имя атрибута.
        - value: Значение атрибута.

        Raises:
        - ValueError: Если атрибут - confirm_password, и значение не совпадает с паролем.
        """
        if name == 'confirm_password':
            if 'password' in self.__dict__ and value != self.__dict__['password']:
                raise ValueError("Password and confirmation password do not match")
        super().__setattr__(name, value)


class UserLogin(BaseModel):
    """
    Модель для авторизации пользователя.
    """
    email_or_phone: str
    password: str
