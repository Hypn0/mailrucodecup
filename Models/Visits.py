from Models import BaseModel, sqlite_db
from peewee import *
from Models.Users import User
from Models.Locations import Location


class Visit(BaseModel):

    id          = IntegerField()
    location    = ForeignKeyField(Location, to_field="id")
    user        = ForeignKeyField(User, to_field="id")
    visited_at  = FloatField()
    mark        = IntegerField()


    class Meta:
        database = sqlite_db

sqlite_db.create_tables([Visit], safe=True)
