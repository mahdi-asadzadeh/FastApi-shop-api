import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict
from typing import Any, List


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class GalleryBase(BaseModel):
    image: str


class Gallery(GalleryBase):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ProductBase(BaseModel):
    title: str
    body: str
    image: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdata(BaseModel):
    title: str
    body: str
    price: float


class ProductList(ProductBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ProductDetail(ProductBase):
    id: int
    galleries: List[Gallery] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
