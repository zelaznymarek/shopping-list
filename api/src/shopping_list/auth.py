from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from shopping_list.db.models import User
from shopping_list.db.session import get_db
from shopping_list.schemas import TokenData

SECRET_KEY = "1be3773b21c25858e2a5a1cbcd058dc267cc81c1ee1e499984c77b74db01bf62"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db_session: Session, email: str):
    return db_session.query(User).filter(User.email == email).first()


def authenticate_user(db_session: Session, *, email: str, password: str):
    user = get_user(db_session, email)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def is_decoded_token_valid(decoded_token: dict) -> bool:
    username = decoded_token.get("sub")
    expiration = decoded_token.get("exp")

    if expiration is None:
        return False

    if expiration < datetime.utcnow().timestamp():
        return False

    if username is None:
        return False

    return True


def get_current_user(
    db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not is_decoded_token_valid(payload):
            raise credentials_exception

        token_data = TokenData(username=payload.get("sub"))
    except JWTError:
        raise credentials_exception

    user = get_user(db_session, token_data.username)

    if user is None:
        raise credentials_exception

    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)):
    user = current_user

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user does not have enough privileges",
        )

    return user
