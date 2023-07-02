from peewee import Model, PostgresqlDatabase
from src.database.config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT


database = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)


class BaseModel(Model):
    class Meta:
        database = database
