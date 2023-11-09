from tortoise import models, fields

from bb.products.models import Product


class ShoppingCart(models.Model):
    """
    Модель корзины.

    Атрибуты:
    - user (User): Пользователь, которому принадлежит корзина.
    - products (list[Product]): Товары в корзине.

    Методы:
    - total_price (property): Возвращает общую стоимость товаров в корзине.
    - add_product(product: Product): Добавляет товар в корзину.
    - remove_product(product: Product): Удаляет товар из корзины.
    - clear_cart(): Очищает корзину.

    """
    user = fields.ForeignKeyField(model_name='bb.users.models.User', related_name='shopping_cart')
    products = fields.ManyToManyField(model_name='bb.products.models.Product', related_name='carts')

    @property
    async def total_price(self) -> float:
        """
        Возвращает общую стоимость товаров в корзине.
        """
        return sum(await Product.filter(carts=self).values_list('price', flat=True))

    async def add_product(self, product: Product) -> None:
        """
        Добавляет товар в корзину.
        """
        if product not in self.products:
            await self.products.add(product)

    def remove_product(self, product: Product) -> None:
        """
        Удаляет товар из корзины.
        """
        self.products.remove(product)

    def clear_cart(self) -> None:
        """
        Очищает корзину.
        """
        self.products.clear()
