from jwt import decode
from config.env import SECRECT_KEY, ALGORITHM

async def verify_jwt_login(token:str) -> dict:
    decoded_token =  decode(token, SECRECT_KEY, ALGORITHM)
    return decoded_token