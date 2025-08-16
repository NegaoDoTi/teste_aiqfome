from services.clients_service import ClientsService
from validators.validate_password import verify_password
from auth.auth_handlers import generate_access_token

class LoginController():
    """Classe responsavel por controllar a rota login
    """
    
    def __init__(self):
        self.clients_service = ClientsService()
        
    async def login_client(self, email:str, password:str) -> str | dict:
        """Efetua o login do cliente utilizando JWT com validação 

        Args:
            email (str): email do cliente
            password (str): senha do cliente

        Returns:
            str | dict: retorna string caso ocorra algo de errado
        """
        
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
        
        