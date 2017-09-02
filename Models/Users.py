from Models import BaseModel, sqlite_db
from peewee import *



class User(BaseModel):

    id          = IntegerField()
    email       = CharField(100)
    first_name  = CharField(50)
    last_name   = CharField(50)
    gender      = CharField(1)
    birth_date  = FloatField()

    class Meta:
        database = sqlite_db

sqlite_db.create_tables([User], safe=True)

