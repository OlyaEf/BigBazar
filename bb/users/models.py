from tortoise import fields, models
from pydantic import BaseModel
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
    """
    name: str
    email: str
    phone: str
    password: str


class UserLogin(BaseModel):
    """
    Модель для авторизации пользователя.
    """
    email_or_phone: str
    password: str
