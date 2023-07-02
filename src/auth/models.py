import uuid

from peewee import UUIDField, TextField

from src.database.common import BaseModel


class User(BaseModel):
    id = UUIDField(null=False, unique=True, primary_key=True, default=uuid.uuid4)
    username = TextField(null=False, unique=True)
    full_name = TextField(null=False)
    email = TextField(null=False, unique=True)
    hashed_password = TextField(null=False)
