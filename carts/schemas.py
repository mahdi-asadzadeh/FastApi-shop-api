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


class AddToCart(BaseModel):
    product_id: int
    quantity: int


class CartItems(BaseModel):
    user_id: str
    product_id: str
    product_image: str
    product_price: str
    product_quantity: str
    row_id: str


class Carts(BaseModel):
    total_price: float
    items: List[CartItems] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        