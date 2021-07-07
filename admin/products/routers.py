from typing import List, Optional
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from accounts.authentication import get_current_user_admin
from pydantic.types import NonNegativeFloat
from starlette.responses import JSONResponse
from werkzeug.utils import secure_filename
from products import schemas
from products import cruds
from database import get_db
import uuid, shutil


router = APIRouter(
    tags=['Admin Products'],
    prefix='/admin/products',
    dependencies=[Depends(get_current_user_admin)],
)


@router.post('/create', response_model=schemas.ProductDetail, dependencies=[Depends(get_db)])
def create(   
    title: str = Form(...),
    body: str = Form(...),
    image: str = Form(...),
    price: float = Form(...), 
    galleries: List[UploadFile] = File(...)):
  
    return cruds.create_product(
        title,
        body,
        image,
        price,
        galleries
    )


@router.get('/list', response_model=List[schemas.ProductList], dependencies=[Depends(get_db)])
def list(skip: int = 0, limit: int = 100):
    return cruds.get_products(skip=skip, limit=limit)


@router.delete('/delete/{product_id}')
def delete(product_id: int):
    cruds.delete_product(product_id=product_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "User delete."})


@router.put('/update/{product_id}', response_model=schemas.ProductDetail, dependencies=[Depends(get_db)])
async def update(
    product_id: int, 
    title: Optional[str] = None,
    body: Optional[str] = None,
    price: Optional[float] = None, 
    image: UploadFile = File(None)
    ):
    if image:
        filename = f'media/products/{uuid.uuid1()}_{secure_filename(image.filename)}'
        with open(f'{filename}', 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
    product = cruds.get_product(product_id)
    product.title = title or product.title
    product.price = price or product.price
    product.body = body or product.body
    product.image = filename or product.image
    product.save()
    return product


@router.get('/detail/{product_id}', response_model=schemas.ProductDetail, dependencies=[Depends(get_db)])
async def product(product_id: int):
    return cruds.get_product(product_id)
