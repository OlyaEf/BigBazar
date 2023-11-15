import logging
from typing import List, Optional

from tortoise.exceptions import IntegrityError

from bb.products.models import Product
from bb.products.schemas import ProductCreateUpdateSchema, ProductPartialUpdateSchema


# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductService:
    """
   Сервис для работы с продуктами в базе данных.
   """
    @staticmethod
    async def create_product(product_data: ProductCreateUpdateSchema, owner_id: int) -> Product:
        """
        Создает новый продукт в базе данных.

        Параметры:
            product_data (ProductCreateUpdateSchema): Схема с данными продукта для создания.
                - name (str): Название продукта.
                - description (str): Описание продукта.
                - price (Decimal): Цена продукта.
            owner_id (int): ID владельца продукта.

        Возвращает:
            Product: Объект созданного продукта.

        Исключения:
            ValueError: Ошибка создания продукта из-за проблем с уникальностью данных или других ограничений базы данных.
        """
        try:
            product = await Product.create(**product_data.model_dump(), owner_id=owner_id)
            return product
        except IntegrityError as e:
            logging.error(f"Error creating product: {e}")
            raise ValueError("Error when creating a product")

    @staticmethod
    async def update_product(product_id: int, product_data: ProductPartialUpdateSchema) -> Optional[Product]:
        """
        Обновляет данные существующего продукта по его ID.

        Параметры:
            product_id (int): Уникальный идентификатор продукта для обновления.
            product_data (ProductPartialUpdateSchema): Схема с данными для обновления продукта.
                - name (str, optional): Новое название продукта.
                - description (str, optional): Новое описание продукта.
                - price (Decimal, optional): Новая цена продукта.

        Возвращает:
            Optional[Product]: Обновленный объект продукта или None, если продукт не найден.

        Логирует:
            Предупреждение, если продукт с указанным ID не найден.
        """
        product = await Product.get_or_none(id=product_id)
        if product:
            for attr, value in product_data.model_dump(exclude_unset=True).items():
                setattr(product, attr, value)
            await product.save()
            return product
        logger.warning(f"Product not found for update: {product_id}")
        return None

    @staticmethod
    async def delete_product(product_id: int) -> bool:
        """
        Удаляет продукт из базы данных по его ID.

        Параметры:
            product_id (int): Уникальный идентификатор продукта для удаления.

        Возвращает:
            bool: True, если продукт успешно удален, False, если продукт не найден.
        """
        product = await Product.get_or_none(id=product_id)
        if product:
            await product.delete()
            return True
        return False

    @staticmethod
    async def get_active_products(limit: int = 10, offset: int = 0) -> List[Product]:
        """
        Получает список активных продуктов с пагинацией.

        Параметры:
            - limit (int, optional): Максимальное количество продуктов для возврата.
            - offset (int, optional): Смещение начала списка продуктов (для пагинации).

        Возвращает:
            List[Product]: Список активных продуктов.
        """
        return await Product.filter(is_active=True).offset(offset).limit(limit).all()

    @staticmethod
    async def set_product_active_status(product_id: int, is_active: bool) -> Optional[Product]:
        """
        Устанавливает или изменяет статус активности продукта.

        Параметры:
            - product_id (int): Уникальный идентификатор продукта.
            - is_active (bool): Статус активности для установки.

        Возвращает:
            Optional[Product]: Обновленный объект продукта или None, если продукт не найден.
        """
        product = await Product.get_or_none(id=product_id)
        if product:
            product.is_active = is_active
            await product.save()
            return product
        return None

    @staticmethod
    async def toggle_product_status(product_id: int) -> Optional[Product]:
        """
        Переключает статус активности продукта (активный/неактивный).

        Параметры:
            product_id (int): Уникальный идентификатор продукта для переключения статуса.

        Возвращает:
            Optional[Product]: Объект продукта с обновленным статусом или None, если продукт не найден.
        """
        product = await Product.get_or_none(id=product_id)
        if product:
            product.is_active = not product.is_active
            await product.save()
            return product
        return None
