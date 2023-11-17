from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "shoppingcart" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "shoppingcart" IS 'Модель корзины.';
        CREATE TABLE "shoppingcart_product" (
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "shoppingcart_id" INT NOT NULL REFERENCES "shoppingcart" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "shoppingcart_product";
        DROP TABLE IF EXISTS "shoppingcart";"""
