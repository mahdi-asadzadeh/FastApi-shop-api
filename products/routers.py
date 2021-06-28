from typing import List
from fastapi import APIRouter, Depends
from database import get_db
from . import schemas
from . import cruds


router = APIRouter(
    tags=['Products'],
    prefix='/products'
)



@router.get('/list', response_model=List[schemas.ProductList], dependencies=[Depends(get_db)])
async def products(skip: int = 0, limit: int = 100):
    return cruds.get_products(skip=skip, limit=limit)


@router.get('/detail/{product_id}', response_model=schemas.ProductDetail, dependencies=[Depends(get_db)])
async def product(product_id: int):
    return cruds.get_product(product_id)
