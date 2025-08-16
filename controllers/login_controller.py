from services.clients_service import ClientsService
from validators.validate_password import verify_password
from auth.auth_handlers import generate_access_token

class LoginController():
    def __init__(self):
        self.clients_service = ClientsService()
        
    async def login_client(self, email:str, password:str) -> str | dict:
        client = await self.clients_service.find_client(email=email)
        
        if client == None:
            return "Cliente não cadastrado"
        
        if not verify_password(password, client.password):
            return "Email ou senha incorretos!"
        
        token = generate_access_token(client.id, client.email)
        
        return {
            "token" : token,
            "type" : "Bearer"
        }
        
        