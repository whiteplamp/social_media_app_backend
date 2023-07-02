from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.schemas import UserInSystem
from src.auth.utils import get_current_user
from src.posts.schemas import Actions
from src.posts.utils import get_posts_from_db, get_post_from_db, create_post_in_db, update_post_in_db, \
    delete_post_in_db, like_or_dislike_post_in_db
from src.posts import schemas

router = APIRouter()


@router.get('/posts')
def get_posts():
    return get_posts_from_db()


@router.get('/post/{post_id}')
def get_post(post_id: str):
    return get_post_from_db(post_id)


@router.post('/post')
def create_post(
        post: schemas.Post,
        current_user: Annotated[UserInSystem, Depends(get_current_user)]
):
    return create_post_in_db(post, current_user)


@router.put('/post/{post_id}')
def update_post(
        post_id: str,
        post: schemas.Post,
        current_user: Annotated[UserInSystem, Depends(get_current_user)]
):
    return update_post_in_db(post_id, post, current_user)


@router.delete('/post/{post_id}')
def delete_post(
        post_id: str,
        current_user: Annotated[UserInSystem, Depends(get_current_user)]
):
    return delete_post_in_db(post_id, current_user)


@router.post('/post/{post_id}/like')
def like_post(
        post_id: str,
        current_user: Annotated[UserInSystem, Depends(get_current_user)]
):
    return like_or_dislike_post_in_db(post_id, current_user, Actions.like.name)


@router.post('/post/{post_id}/dislike')
def dislike_post(
        post_id: str,
        current_user: Annotated[UserInSystem, Depends(get_current_user)]
):
    return like_or_dislike_post_in_db(post_id, current_user, Actions.dislike.name)

