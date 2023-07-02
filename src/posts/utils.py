import uuid
from datetime import datetime

from fastapi import HTTPException
from starlette import status

from src.auth.models import User
from src.auth.schemas import UserInSystem
from src.database.common import database
from src.posts import schemas
from src.posts.logger import logger
from src.posts.models import Post, LikeOrDislikePost
from src.posts.schemas import Actions


def get_likes_quantity(post_id: str) -> int:
    return LikeOrDislikePost.select().where(
        (LikeOrDislikePost.post_id == post_id) &
        (LikeOrDislikePost.action_type == Actions.like.name)
    ).count()


def get_dislikes_quantity(post_id: str) -> int:
    return LikeOrDislikePost.select().where(
        (LikeOrDislikePost.post_id == post_id) &
        (LikeOrDislikePost.action_type == Actions.dislike.name)
    ).count()


def get_posts_from_db() -> list[dict]:
    with database.atomic():
        posts_data = []
        posts = Post.select().order_by(Post.updated_at)
        for post in posts:
            user = User.select().where(User.id == post.user_id).get_or_none()
            likes_quantity = get_likes_quantity(post.id)
            dislikes_quantity = get_dislikes_quantity(post.id)

            if not user:
                continue
            posts_data.append({
                'post_id': post.id,
                'text': post.text,
                'created_by': user.username,
                'created_at': post.created_at,
                'updated_at': post.created_at,
                'likes': likes_quantity,
                'dislikes': dislikes_quantity,
            })
    return posts_data


def get_post_from_db(post_id: str) -> dict:
    with database.atomic():
        post = Post.select().where(Post.id == post_id).get_or_none()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Post does not exists"
            )
        user = User.select().where(User.id == post.user_id).get_or_none()
        return {
            'post_id': post.id,
            'text': post.text,
            'created_by': user.username,
            'created_at': post.created_at,
            'updated_at': post.created_at,
            'likes': get_likes_quantity(post_id),
            'dislikes': get_dislikes_quantity(post.id),
        }


def create_post_in_db(post: schemas.Post, user: UserInSystem) -> dict:
    with database.atomic():
        creation_time = datetime.utcnow()
        post_id = uuid.uuid4()
        Post.insert({
            'id': post_id,
            'text': post.text,
            'user_id': user.id,
            'created_at': creation_time,
            'updated_at': creation_time,
        }).execute()
        logger.info(f"User {user.username} created post {post_id}")
    return {
        'post_id': post_id
    }


def update_post_in_db(post_id: str, post: schemas.Post, user: UserInSystem) -> dict:
    with database.atomic():
        post_in_db = Post.select().where(Post.id == post_id).get_or_none()
        if post_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Post does not exists"
            )
        if str(post_in_db.user_id) != user.id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="User have not rights on this post"
            )
        Post.update({
            'text': post.text,
            'updated_at': datetime.utcnow()
        }).where(Post.id == post_id).execute()

        return {
            'post_id': post_id
        }


def delete_post_in_db(post_id: str, user: UserInSystem) -> dict:
    with database.atomic():
        post_in_db = Post.select().where(Post.id == post_id).get_or_none()
        if post_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Post does not exists"
            )
        if str(post_in_db.user_id) != user.id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="User have not rights on this post"
            )
        Post.delete().where(Post.id == post_id).execute()
        return {
            'post_id': post_id
        }


def like_or_dislike_post_in_db(post_id: str, user: UserInSystem, action: str) -> dict:
    with database.atomic():
        post_in_db = Post.select().where(Post.id == post_id).get_or_none()
        if post_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Post does not exists"
            )
        if user.id == post_in_db.user_id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="You can not like your own post"
            )
        like_or_dislike = LikeOrDislikePost.select().where(
            (LikeOrDislikePost.post_id == post_id) &
            (LikeOrDislikePost.user_id == user.id)
        ).get_or_none()

        if not like_or_dislike:
            LikeOrDislikePost.insert({
                'post_id': post_id,
                'user_id': user.id,
                'action_type': action
            }).execute()
        else:
            LikeOrDislikePost.update({
                'action_type': action
            }).where(
                (LikeOrDislikePost.post_id == post_id) &
                (LikeOrDislikePost.user_id == user.id)
            ).execute()

    return {
        'post_id': post_id
    }

