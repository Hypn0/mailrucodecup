from peewee import *
sqlite_db = SqliteDatabase(':memory:')

class BaseModel(Model):
    class Meta:
        database = sqlite_db