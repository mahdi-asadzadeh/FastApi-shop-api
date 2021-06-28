import peewee
from database import db


class Product(peewee.Model):
    title = peewee.CharField(max_length=50)
    body = peewee.TextField()
    image = peewee.CharField(max_length=100, unique=True)
    price = peewee.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = db


class Gallery(peewee.Model):
    product = peewee.ForeignKeyField(Product, on_delete='CASCADE', backref='galleries')
    image = peewee.CharField(max_length=100, unique=True)
    
    class Meta:
        database = db
