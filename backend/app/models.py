import enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .db import Base


class ProviderNames(str, enum.Enum):
    monobank = "monobank"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(40), unique=True, index=True)
    hashed_password = Column(String(60))
    is_active = Column(Boolean, default=True)

    accounts = relationship("Account")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(ProviderNames))
    api_key = Column(String(255))


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    original_id = Column(String, index=True, nullable=True)  # ID by provider
    provider_id = Column(Integer, ForeignKey("providers.id"))

    balance = Column(Integer)
    creditLimit = Column(Integer)
    currencyCode = Column(Integer)  # ISO 4217
    cashbackType = Column(String)  # Possible values:  None, UAH, Miles

    provider = relationship("Provider")
    statements = relationship("Statement")


class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    time = Column(DateTime)
    description = Column(String)
    mcc = Column(Integer)
    amount = Column(Integer)
    operationAmount = Column(Integer)
    currencyCode = Column(Integer)
    commissionRate = Column(Integer)
    cashbackAmount = Column(Integer)
    balance = Column(Integer)
