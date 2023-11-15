from tortoise import models, fields
from bb.products.models import Product


class ShoppingCart(models.Model):
    """
    Модель корзины.

    Атрибуты:
    - user (User): Пользователь, которому принадлежит корзина.
    - products (ManyToManyField[Product]): Товары в корзине.

    Методы:
    - total_price (property): Возвращает общую стоимость товаров в корзине.
    - add_product(product: Product | List[Product]): Добавляет один товар или список товаров в корзину.
    - remove_product(product: Product): Асинхронно удаляет товар из корзины.
    - clear_cart(): Асинхронно очищает корзину.
    """
    user = fields.ForeignKeyField(model_name='models.User', related_name='shopping_cart')
    products = fields.ManyToManyField(model_name='models.Product', related_name='carts')

    @property
    async def total_price(self) -> float:
        """
        Возвращает общую стоимость товаров в корзине.
        """
        return sum(await Product.filter(carts=self).values_list('price', flat=True))

    async def add_product(self, products) -> None:
        """
        Добавляет один товар или список товаров в корзину.
        """
        if isinstance(products, Product):
            products = [products]

        for product in products:
            if product not in await self.products.all():
                await self.products.add(product)

    async def remove_product(self, product: Product) -> None:
        """
        Асинхронно удаляет товар из корзины.
        """
        await self.products.remove(product)

    async def clear_cart(self) -> None:
        """
        Асинхронно очищает корзину.
        """
        await self.products.clear()
