from typing import Union

from sqlalchemy.orm import Session

from app import schemas, models
from app.utils import get_password_hash


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_username(db: Session, username: str) -> Union[models.User, None]:
    return db.query(models.User).filter_by(username=username).first()


def create_account_for_user(db: Session, account: schemas.AccountCreate, user: schemas.User, provider: str):
    db_account = models.Account(
        **account.dict(),
        owner_id=user.id,
        provider=provider,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


def get_account_by_id(db: Session, id_: int) -> Union[models.Account, None]:
    return db.query(models.Account).filter_by(id=id_).first()


def get_accounts_for_user(db: Session, user_id: int) -> Union[models.Account, None]:
    return db.query(models.Account).filter_by(owner_id=user_id).all()
