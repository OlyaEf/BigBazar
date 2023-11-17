from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

from bb.users.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Получает текущего аутентифицированного пользователя по токену JWT.

    Параметры:
        token (str): Токен доступа JWT.

    Возвращает:
        User: Экземпляр модели User, представляющий аутентифицированного пользователя.

    Вызывает:
        HTTPException: Если токен недействителен или пользователь не найден.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.get_or_none(email=username)
    if user is None:
        raise credentials_exception
    return user

