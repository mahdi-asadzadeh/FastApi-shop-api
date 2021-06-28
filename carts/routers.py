from accounts.authentication import get_current_user
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from database import get_db
from . import schemas
from .cart import Cart
from decimal import Decimal
from products.cruds import get_product
from accounts.schemas import User


router = APIRouter(
    tags=['Carts'],
    prefix='/carts'
)


@router.post('/add', dependencies=[Depends(get_db)])
async def add_to_cart(add_to_cart: schemas.AddToCart, user: User = Depends(get_current_user)):
    product = get_product(add_to_cart.product_id)
    Cart.add_to_cart(
        user_id = user.id,
        product_id = product.id,
        product_image = str(product.image),
        product_price = str(Decimal(product.price) * add_to_cart.quantity),
        product_quantity = add_to_cart.quantity,
	)
    content = {'message': 'Add to cart.'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get('/list', response_model=schemas.Carts)
async def carts(user: User = Depends(get_current_user)):
    total_price = 0
    items = Cart.carts(user.id)
    for item in items:
        total_price += float(item['product_price'])

    return {'total_price': total_price, 'items': items}


@router.delete('/clear')
async def clear_cart(user: User = Depends(get_current_user)):
    Cart.delete_all_carts(user.id)
    content = {'message': 'Clear carts.'}
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=content)


@router.delete('/delete-item-cart/{row_id}')
async def delete_item_cart(row_id: str, user: User = Depends(get_current_user)):
    Cart.delete_cart(user.id, row_id)
    content = {'message': 'Delete item cart.'}
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=content)
