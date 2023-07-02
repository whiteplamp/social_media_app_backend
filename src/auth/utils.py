import binascii
import hashlib
import os
from datetime import timedelta, datetime

from fastapi import HTTPException, security, Security
from jose import jwt, JWTError
from peewee import IntegrityError
from starlette import status

from src.auth.config import JWT_AUTH_SECRET_KEY, JWT_AUTH_ALGORITHM
from src.auth.exceptions import DuplicateUserException, UserDoesNotExistException, IncorrectPasswordException
from src.auth.models import User
from src.auth.schemas import UserSignUp, UserSignIn, UserInSystem
from src.database.common import database
from src.auth.logger import logger


token_key = security.APIKeyHeader(name="Authorization")


def hash_password(password: str) -> str:
    salt = b'__hash__' + hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    salt = stored_password[:72]
    stored_password = stored_password[72:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def register_user(form_data: UserSignUp):
    with database.atomic() as transaction:
        try:
            User.insert({
                "username": form_data.username,
                "full_name": form_data.full_name,
                "email": form_data.email,
                "hashed_password": hash_password(form_data.password)
            }).execute()
        except IntegrityError:
            transaction.rollback()
            logger.error("User already exists")
            raise DuplicateUserException("User already exists")


def authenticate_user(form_data: UserSignIn):
    with database.atomic():
        user = User.select().where(User.username == form_data.username).get_or_none()
    if not user:
        logger.error("User does not exists")
        raise UserDoesNotExistException("User does not exist")

    try:
        assert verify_password(user.hashed_password, form_data.password) == True
    except AssertionError:
        logger.error("Passwords does not match")
        raise IncorrectPasswordException("Passwords does not match")


def generate_jwt_token(data: dict, expires_delta: timedelta | None = None) -> dict:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=8)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_AUTH_SECRET_KEY, algorithm=JWT_AUTH_ALGORITHM)
    return {
        "access_token": encoded_jwt,
        "token_type": 'bearer'
    }


def get_current_user(encoded_jwt: str = Security(token_key)) -> UserInSystem:
    try:
        try:
            jwt_token = encoded_jwt.split(' ')[1]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = jwt.decode(jwt_token, JWT_AUTH_SECRET_KEY, algorithms=[JWT_AUTH_ALGORITHM,])
        username = payload.get('sub')
        expires_in = datetime.fromtimestamp(payload.get("exp") / 1e3)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if expires_in > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token had expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User.select().where(User.username == username).get_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist"
        )

    return UserInSystem(id=str(user.id), username=user.username)
