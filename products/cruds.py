import shutil
from fastapi import HTTPException, status
from werkzeug.utils import secure_filename
from products import schemas
from . import models
import uuid

def get_products(skip: int = 0, limit: int = 100):
    return list(models.Product.select().offset(skip).limit(limit))


def create_product( 
        title,
        body,
        image,
        price,
        galleries
        ):
    db_product = models.Product(
        title=title,
        body=body,
        image=image,
        price=price
    )
    db_product.save()
    for image in galleries:
        upload_image_product(image, db_product.id)
    return db_product


def upload_image_product(image, product_id):
    filename = f'media/product_galleries/{uuid.uuid1()}_{secure_filename(image.filename)}'
    with open(f'{filename}', 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
    models.Gallery(product=product_id, image=filename).save()


def delete_product(product_id: int):
    product = models.Product.filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    product.delete_instance()
    return 'Done.'


def get_product(product_id: int):
    product = models.Product.filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    return product
