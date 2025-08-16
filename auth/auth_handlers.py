from passlib.context import CryptContext
from datetime import datetime, timedelta
from config.env import SECRECT_KEY, ALGORITHM
from zoneinfo import ZoneInfo
import jwt

pwd_context = CryptContext(schemes=["bcrypt"])

def generate_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def generate_access_token(client_id:int, client_email:str, expires_time: timedelta = timedelta(hours=1)) -> str:
    
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    expire = now + expires_time
    
    payload = {
        "client_id" : client_id,
        "client_email" : client_email,
        "iat" : now,
        "exp" : expire
    }
    
    encode_jwt = jwt.encode(payload, SECRECT_KEY, ALGORITHM)
    
    return encode_jwt