import os

from dotenv import load_dotenv

load_dotenv()

# Database

POSTGRES_DB: str = os.getenv("POSTGRES_DB", "db_bigbazar")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)

DATABASE_LOGIN = f"asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
DATABASE_CONNECT = f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATABASE_URL = DATABASE_LOGIN + DATABASE_CONNECT


MODELS = [
    "bb.users.models",
    "bb.products.models",
    "bb.cart.models",
]

# Tortoise ORM settings
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                *MODELS,
                "aerich.models"
            ],
            "default_connection": "default",
            "generate_schemas": True,
            "add_exception_handlers": False,
        },
    },
}

