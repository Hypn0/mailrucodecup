from Models import BaseModel, sqlite_db
from peewee import *



class Location(BaseModel):

    id       = IntegerField()
    place    = TextField()
    country  = CharField(50)
    city     = CharField(50)
    distance = IntegerField()


    class Meta:
        database = sqlite_db

sqlite_db.create_tables([Location], safe=True)

