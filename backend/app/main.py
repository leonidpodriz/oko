from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, models, crud
from .services.user_service import UserService
from .services.provider_service import ProviderSerivce
from .crud import create_user, create_account_for_user
from .db import engine
from .dependencies import get_db, get_current_active_user, get_user_accounts
from .schemas import User, Account, AccountCreate, ProviderBase
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .utils import authenticate_user, create_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def status_ok():
    return {"status": "OK"}


@app.post("/register", response_model=schemas.User, tags=["auth"])
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user_data.username)

    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    return create_user(db, user_data)


@app.post("/login", response_model=schemas.Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.from_username(db, form_data.username)
    user.authenticate_user(form_data.password)
    access_token = user.create_access_token()

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=User, tags=["user"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/accounts", response_model=List[Account], tags=["account"])
def get_accounts(accounts: List[Account] = Depends(get_user_accounts)):
    return accounts


@app.post("/accounts", response_model=Account, tags=["account"])
def create_account(account: AccountCreate, current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    return create_account_for_user(db, account, current_user, "user")


@app.get("/accounts/{idx}", tags=["account", "statements"])
def get_account_statements(idx: int, current_user: User = Depends(get_current_active_user)):
    return idx


@app.post("/integrate/", tags=["integrations"])
def integrate(provider_data: ProviderBase):
    provider = ProviderSerivce(provider_data).get_provider()
    if not provider.is_valid(provider_data):
        raise HTTPException(
            status_code=400, detail="Provider is not valid"
        )
    return None
