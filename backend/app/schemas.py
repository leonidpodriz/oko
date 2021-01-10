import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, Field
from .models import ProviderNames


# === Token ===
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# == User ===
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    accounts: List[Any]

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


# === Statements ===
class StatementBase(BaseModel):
    account_id: int
    time: datetime.datetime
    description: str
    mcc: int
    amount: int
    operationAmount: int
    currencyCode: int
    commissionRate: int
    cashbackAmount: int
    balance: int


class StatementCreate(StatementBase):
    pass


class Statement(StatementBase):
    id: int

    class Config:
        orm_mode = True


# === Account ===
class AccountBase(BaseModel):
    original_id: Optional[str]
    balance: int
    creditLimit: int
    currencyCode: int
    cashbackType: int


class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True


class AccountWithStatements(AccountBase):
    statements: List[Statement]

    class Config:
        orm_mode = True


class AccountCreate(AccountBase):
    pass


# === Provider ===
class ProviderBase(BaseModel):
    name: ProviderNames
    api_key: str = Field(..., max_lenght=255)


class Provider(ProviderBase):
    id: int
