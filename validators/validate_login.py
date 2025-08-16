from jwt import decode
from config.env import SECRECT_KEY, ALGORITHM

async def verify_jwt_login(token:str) -> dict:
    """Verifica se o cliente esta logado

    Args:
        token (str): token JWT

    Returns:
        dict: payload descriptografado
    """
    
    decoded_token =  decode(token, SECRECT_KEY, ALGORITHM)
    return decoded_token