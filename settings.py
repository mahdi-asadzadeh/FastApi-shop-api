from decouple import config


JWT_SECRET =  config('JWT_SECRET') 
EXPIRED_TIME = 900  # 15 minute
