import uuid

from peewee import UUIDField, TextField, ForeignKeyField, DateTimeField

from src.auth.models import User
from src.database.common import BaseModel


class Post(BaseModel):
    id = UUIDField(null=False, unique=True, primary_key=True, default=uuid.uuid4)
    text = TextField(null=False)
    user_id = ForeignKeyField(User, backref='post')
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)


class LikeOrDislikePost(BaseModel):
    post_id = ForeignKeyField(Post)
    user_id = ForeignKeyField(User)
    action_type = TextField(null=False)
