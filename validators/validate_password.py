from auth.auth_handlers import pwd_context

def verify_password(password:str, hash_password:str):
    return pwd_context.verify(password, hash_password)