from typing import List
from decouple import config
from fastapi_mail import ConnectionConfig
from fastapi import FastAPI

from carts.routers import router as carts_router

from order.models import Order, OrderItem
from order.routers import router as orders_routers

from accounts.models import User
from accounts.routers import router as users_routers

from products.models import Product, Gallery
from products.routers import router as products_routers

from admin.products.routers import router as admin_products_routers
from admin.accounts.routers import router as admin_accounts_routers

from database import db_state_default
import database


database.db.connect()
database.db.create_tables([User, Product, Gallery, Order, OrderItem])
database.db.close()


app = FastAPI()


conf = ConnectionConfig(
   MAIL_USERNAME=config('MAIL_USERNAME'),
   MAIL_PASSWORD=config('MAIL_PASSWORD'),
   MAIL_FROM=config('MAIL_FROM'),
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False
)


app.include_router(carts_router)
app.include_router(users_routers)
app.include_router(products_routers)
app.include_router(orders_routers)
app.include_router(admin_products_routers)
app.include_router(admin_accounts_routers)
