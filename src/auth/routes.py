from fastapi import APIRouter, HTTPException
from starlette import status

from src.auth.exceptions import UserDoesNotExistException, IncorrectPasswordException, DuplicateUserException
from src.auth.schemas import UserSignUp, UserSignIn
from src.auth.utils import register_user, generate_jwt_token, authenticate_user

router = APIRouter()


@router.post('/sign_up')
def sign_up(form_data: UserSignUp):
    try:
        register_user(form_data)
    except DuplicateUserException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return generate_jwt_token({'sub': form_data.username})


@router.post('/sign_in')
def sigh_in(form_data: UserSignIn):
    try:
        authenticate_user(form_data)
    except UserDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exists",
        )
    except IncorrectPasswordException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_jwt_token({'sub': form_data.username})
