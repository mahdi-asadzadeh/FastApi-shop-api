from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from accounts.authentication import get_current_user
from .models import Order, OrderItem
from products.models import Product
from accounts.schemas import User
from database import get_db
from carts.cart import Cart


router = APIRouter(
    tags=['Orders'],
    prefix='/orders'
)


@router.get('/list', dependencies=[Depends(get_db)])
async def list_order(user: User = Depends(get_current_user)):
    orders = Order.filter(Order.user == user)
    return orders


@router.post('/create', dependencies=[Depends(get_db)])
async def create_order(address: str, user: User = Depends(get_current_user)):
    carts = Cart.carts(user.id)
    if carts == []:
        content = {'error': 'carts are empty.'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    total_price = 0
    for cart in carts:
        total_price += float(cart['product_price'])
    order = Order.objects.create(
        user=user,
        price=total_price,
        paid=False,
        address=address,
        )
    for cart in carts:
        OrderItem.objects.create(
            product=cart['product_id'],
            order=order.id,
        )
    Cart.delete_all_carts(user.id)
    content = {'massage': 'create order.'}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
