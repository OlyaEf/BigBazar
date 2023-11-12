from tortoise import fields, models
from passlib.hash import bcrypt


class User(models.Model):
    """
    Модель пользователя для хранения информации о пользователях в базе данных.

    Атрибуты:
        - name (str): Имя пользователя, максимальная длина 150 символов.
        - email (str): Уникальный электронный адрес пользователя.
        - phone (str): Уникальный телефонный номер пользователя.
        - password (str): Хэшированный пароль пользователя.
        - created_at (datetime): Дата и время создания записи пользователя.
        - updated_at (datetime): Дата и время последнего обновления записи пользователя.

    Методы:
        __str__(self) -> str: Возвращает e-mail пользователя в виде строки.
        set_password(self, raw_password: str) -> None: Хэширует и устанавливает пароль пользователя.
        check_password(self, raw_password: str) -> bool: Проверяет пароль пользователя.
        create_user(cls, name: str, email: str, phone: str, password: str) -> 'User':
            Создает и сохраняет нового пользователя в базе данных.
    PydanticMeta:
        exclude (list): Исключает поле пароля из модели Pydantic.
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

    def set_password(self, raw_password):
        """
        Хэширует и устанавливает пароль пользователя.

        Параметры:
            raw_password (str): Нешифрованный пароль пользователя.
        """
        self.password = bcrypt.hash(raw_password)

    def check_password(self, raw_password):
        """
        Проверяет пароль пользователя.

        Параметры:
            raw_password (str): Нешифрованный пароль для проверки.

        Возвращает:
            bool: Возвращает True, если пароль верный, иначе False.
        """
        return bcrypt.verify(raw_password, self.password)

    @classmethod
    async def create_user(cls, name: str, email: str, phone: str, password: str) -> 'User':
        """
        Создает и сохраняет нового пользователя в базе данных.

        Параметры:
            - name (str): Имя пользователя.
            - email (str): Электронный адрес пользователя.
            - phone (str): Телефонный номер пользователя.
            - password (str): Нешифрованный пароль пользователя.

        Возвращает:
            User: Экземпляр созданного пользователя.
        """
        user = cls(name=name, email=email, phone=phone)
        user.set_password(password)
        await user.save()
        return user
