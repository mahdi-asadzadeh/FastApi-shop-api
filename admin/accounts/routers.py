from fastapi import APIRouter, Depends, status
from accounts import cruds, models, schemas
from accounts.authentication import get_current_user_admin
from starlette.responses import JSONResponse
from database import get_db
from typing import List


router = APIRouter(
    tags=['Admin Accounts'], 
    prefix='/admin/accounts',
    dependencies=[Depends(get_current_user_admin)],
)


@router.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
async def read_users(skip: int = 0, limit: int = 100):
    users = cruds.get_users(skip=skip, limit=limit)
    return users


@router.delete('/user/{user_id}')
async def delete_user(user_id: int):
    user = models.User.filter(models.User.id == user_id).first()
    if user:
        user.delete_instance()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "User delete."})
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found."})
