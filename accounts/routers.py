from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from typing import List
from database import get_db
from .authentication import authenticate_user, get_current_user
from .utils import Hash, send_register_email, get_from_redis, token_delete_to_redis
from . import models
from . import schemas
from . import cruds
import jwt
import settings


router = APIRouter(
    tags=['Accounts'], 
    prefix='/accounts'
)


@router.post('/token', dependencies=[Depends(get_db)])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid email or password'
        )
    user = {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'is_admin': user.is_admin
    }
    token = jwt.encode(user, settings.JWT_SECRET)
    return {'access_token' : token, 'token_type' : 'bearer'}


@router.get('/user/me', response_model=schemas.User, dependencies=[Depends(get_db)])
async def detail_user(user: schemas.User = Depends(get_current_user)):
    return user


@router.post("/user/", response_model=schemas.User, dependencies=[Depends(get_db)])
async def register(background_tasks: BackgroundTasks, user: schemas.UserCreate):
    db_user = cruds.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    user = cruds.create_user(user=user)
    send_register_email(
        id=user.id,
        email=user.email,
        background_tasks=background_tasks
    )
    return user


@router.post("/user/activate", dependencies=[Depends(get_db)])
async def activate(data: schemas.Activate):
    user = cruds.get_user_by_email(email=data.email)
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Wrong/Expired Token!."})
        
    token_from_redis = get_from_redis(user.id, 'register')
    if not token_from_redis:
        content = {'message': 'Wrong/Expired Token!.'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    if data.token != token_from_redis.decode('UTF-8'):
        content = {'message': 'Wrong/Expired Token!.'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    user.is_active = True
    user.save()
    token_delete_to_redis(user.id, 'register')
    content = {'message': 'Active account.'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.post('/user/change_password', dependencies=[Depends(get_db)])
async def change_password(data: schemas.ChangePassword, user: schemas.User = Depends(get_current_user)):
    if Hash.verify(data.old_password, user.hashed_password):
        user.hashed_password = Hash.bcrypt(data.new_password)
        user.save()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User change password."})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Old password is incorrect."})
