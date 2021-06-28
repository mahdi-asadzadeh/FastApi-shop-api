import peewee
from database import db


class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=False)
    is_admin = peewee.BooleanField(default=False)

    class Meta:
        database = db
