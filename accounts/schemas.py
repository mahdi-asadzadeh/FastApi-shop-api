from typing import Any, List

import peewee
from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Activate(BaseModel):
    email: EmailStr
    token: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
