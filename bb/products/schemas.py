from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from bb.products.models import Product

ProductRetrieveSchema = pydantic_model_creator(Product, name="Product",  exclude=("is_active",))


class ProductCreateUpdateSchema(BaseModel):
    """
    Схема для создания или обновления продукта.

    Атрибуты:
        - name (str): Название продукта. Должно быть не длиннее 150 символов.
        - description (Optional[str]): Описание продукта. Может быть не указано. Максимальная длина - 350 символов.
        - price (Decimal): Цена продукта. Должна быть больше нуля.
    """
    name: str = Field(..., max_length=150)
    description: Optional[str] = Field(None, max_length=350)
    price: Decimal = Field(..., gt=0)


class ProductPartialUpdateSchema(BaseModel):
    """
    Схема для частичного обновления данных продукта.

    Атрибуты:
        - name (Optional[str]): Новое название продукта. Может быть не указано. Длина до 150 символов.
        - description (Optional[str]): Новое описание продукта. Может быть не указано. Длина до 350 символов.
        - price (Optional[Decimal]): Новая цена продукта. Может быть не указана. Должна быть больше нуля.
    """
    name: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = Field(None, max_length=350)
    price: Optional[Decimal] = Field(None, gt=0)
