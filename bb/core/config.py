import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv(
    "DEBUG", 'False'
).lower() in ('true', '1', 'True')

ALLOWED_HOSTS = ['*']

ALL_HOSTS = "http://*"

# CORS settings
CORS_ALLOWED_ORIGINS = [
    os.getenv('CORS_ALLOWED_HOST', ALL_HOSTS)
]
CORS_ALLOW_ALL_ORIGINS = os.getenv(
    "CORS_ALLOW_ALL_ORIGINS", 'False'
).lower() in ('true', '1', 'True')

# CSRF protection settings
CSRF_TRUSTED_ORIGINS = [
    os.getenv('CSRF_TRUSTED_FRONTEND', ALL_HOSTS),
    os.getenv('CSRF_TRUSTED_BACKEND', ALL_HOSTS)
]

# Database

POSTGRES_DB = os.getenv("POSTGRES_DB", "db_bigbazar")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

DATABASE_LOGIN = f"asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
DATABASE_CONNECT = f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATABASE_URL = DATABASE_LOGIN + DATABASE_CONNECT


MODELS = [
    "bb.users.models",
    "bb.product.models",
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media files uploaded by users / customers
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email settings
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True
