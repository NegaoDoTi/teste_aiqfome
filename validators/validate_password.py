from auth.auth_handlers import pwd_context

def verify_password(password:str, hash_password:str):
    """Verifica se o password e valido com hash

    Args:
        password (str): password em texto
        hash_password (str): password criptografado

    Returns:
        bool: True se for valido se nao False
    """
    
    return pwd_context.verify(password, hash_password)