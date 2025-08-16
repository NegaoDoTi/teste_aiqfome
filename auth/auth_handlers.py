from passlib.context import CryptContext
from datetime import datetime, timedelta
from config.env import SECRECT_KEY, ALGORITHM
from zoneinfo import ZoneInfo
import jwt

pwd_context = CryptContext(schemes=["bcrypt"])

def generate_password_hash(password:str) -> str:
    """Gera o hash de password para salvar no banco de dados

    Args:
        password (str): hash do password

    Returns:
        str: hash do password
    """
    return pwd_context.hash(password)

def generate_access_token(client_id:int, client_email:str, expires_time: timedelta = timedelta(hours=1)) -> str:
    """Gera o token JWT de login com 1 horas de tempo para expirar

    Args:
        client_id (int): id do cliente
        client_email (str): email do cliente
        expires_time (timedelta, optional): Opicional por padrao 1 hora.

    Returns:
        str: token JWT
    """
    
    
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