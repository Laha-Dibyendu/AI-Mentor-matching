from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from typing import Annotated
from pydantic import BaseModel
from user_db import *

# Set up your JWT secret key
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Set up your password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User2(BaseModel):
    username: str
    name: str
    email: str
    password: str

class User3(BaseModel):
    name: str
    email: str

class User4(BaseModel):
    username: str

class UserInDB(BaseModel):
    id: int
    username: str
    name: str
    email: str
    hashed_password: str
    disabled: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


# Define your authentication functions
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/check-token")

# Verifying the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Getting the user from Database
def get_user(username: str):
    data = database_user().user_detail(username)
    if data:
        real_user_db = {
            data["username"]:
            {"id": int(data["id"]),
             "username": data["username"],
             "name": data["full_name"],
             "email": data["email"],
             "hashed_password": data["hashed_password"]
             }}
        if username in real_user_db:
            user_dict = real_user_db[username]
            return UserInDB(**user_dict)
    else:
        return ""

# Authenticating user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Creating Access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Getting current logged in User
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentialssssssssssss",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Checking if the user is active or not
async def get_current_active_user(
    current_user: Annotated[User2, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
