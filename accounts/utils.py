
import os
import redis
import binascii

from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema
from fastapi import BackgroundTasks


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(plain_password, hashed_password):
        return pwd_cxt.verify(plain_password, hashed_password)


redis = redis.Redis.from_url('redis://')


def _generate_code():
	return binascii.hexlify(os.urandom(20)).decode('utf-8')


def send_email(email, token, background_tasks):
    message = MessageSchema(
        subject="Activate Account",
        recipients=[email,],
        body=''.join(token),
        )
    from main import conf
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)


def token_add_to_redis(id, mode):
    token = _generate_code()
    name = f'{id}_{mode.lower()}'
    redis.set(name=name, value=token, ex=14400)
    return token


def token_delete_to_redis(id, mode):
    name = f'{id}_{mode.lower()}'
    redis.delete(name)


def get_from_redis(id, mode):
    name = f'{id}_{mode.lower()}'
    return redis.get(name=name)


def send_register_email(id,  email, background_tasks):
    token_delete_to_redis(id, 'register')
    token = token_add_to_redis(id=id, mode='register'),
    send_email(email=email, token=token, background_tasks=background_tasks)


# def send_reset_password_email(id, email, username, first_name, last_name):
#     token_delete_to_redis(id, 'reset_password')
#     ctxt = {
#         'email': email,
#         'username': username,
#         'first_name': first_name,
#         'last_name': last_name,
#         'token': token_add_to_redis(id, 'reset_password'),
#         'btn_name': 'Reset password . Click Me !'
#     }
#     send_multi_format_email('signup_email', ctxt, target_email=email)


# def send_change_email(id, email, username, first_name, last_name):
#     token_delete_to_redis(id, 'change_email')
#     ctxt = {
#         'email': email,
#         'username': username,
#         'first_name': first_name,
#         'last_name': last_name,
#         'token': token_add_to_redis(id, 'change_email'),
#         'btn_name': 'Change email . Click Me !'
#     }
#     send_multi_format_email('signup_email', ctxt, target_email=email)
