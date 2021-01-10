import datetime
from typing import Optional, Union

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import schemas, settings, crud, models


class UserService:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    UNAUTHORIZED_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    user: schemas.UserInDB

    def __init__(self, user: schemas.UserInDB):
        self.user = user

    def verify_password(self, password: str) -> bool:
        return self._verify_password(password, self.user.hashed_password)

    def authenticate_user(self, password: str, raise_http: bool = True):
        if not self.verify_password(password):
            if raise_http:
                raise self.UNAUTHORIZED_EXCEPTION
            return False

        return True

    def _get_expire_datetime(self, expires_delta: Optional[datetime.timedelta] = None) -> datetime.datetime:
        if expires_delta:
            return datetime.datetime.utcnow() + expires_delta

        return datetime.datetime.utcnow() + self.ACCESS_TOKEN_EXPIRES

    def create_access_token(self, expires_delta: Optional[datetime.timedelta] = None):
        expire_datetime = self._get_expire_datetime(expires_delta)
        to_encode = {
            "sub": self.user.username,
            "exp": expire_datetime,
        }

        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @classmethod
    def _verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.PWD_CONTEXT.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD_CONTEXT.hash(password)

    @classmethod
    def from_username(cls, db: Session, username: str):
        user: Union[models.User, None] = crud.get_user_by_username(db, username)

        if not user:
            raise cls.UNAUTHORIZED_EXCEPTION

        return cls(schemas.UserInDB.from_orm(user))
