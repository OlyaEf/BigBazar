from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "product" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "description" TEXT NOT NULL,
    "price" DECIMAL(10,2) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "product" IS 'Модель, представляющая товар в приложении.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "product";"""
