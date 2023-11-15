from tortoise import fields, models


class Product(models.Model):
    """
    Модель, представляющая товар в приложении.

    Атрибуты:
    - name (str): Название товара (максимум 150 символов).
    - description (str): Описание товара.
    - price (decimal): Цена товара с 2 знаками после запятой.
    - is_active (bool): Указывает, активен ли товар (по умолчанию False).
    - created_at (datetime): Дата и время создания товара.
    - updated_at (datetime): Дата и время последнего обновления товара.
    - owner (models.User): Владелец товара.

    Методы:
    - __str__(): Возвращает название товара в виде строки.

    PydanticMeta:
    - exclude (список): Исключает поля owner, created_at, updated_at, is_active
    из Pydantic-моделей.
    """
    name = fields.CharField(max_length=150)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    owner = fields.ForeignKeyField(
        model_name='models.User', related_name='product'
    )

    def __str__(self) -> str:
        """
        Возвращает название товара в виде строки.
        """
        return self.name

    class PydanticMeta:
        exclude = ['owner', 'created_at', 'updated_at', 'is_active']
