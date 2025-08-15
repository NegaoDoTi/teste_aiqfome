from models.Clients import Clients
from services.clients_service import ClientsService
from auth.auth_handlers import generate_password_hash

class ClientsController():
    def __init__(self):
        self.client_service = ClientsService()
        
    async def registe_client(self, client_name:str, client_email:str, client_password:str) -> Clients | str:
        
        check = await self.client_service.find_client(email=client_email)
        
        if check != None:
            return f"O e-mail '{client_email}' já está sendo usado."
        
        hashed_password = generate_password_hash(client_password)
        
        client = await self.client_service.create_client(client_name, client_email, hashed_password)
        
        return client
    
    async def find_all_clients(self) -> list[dict]:
        clients = await self.client_service.find_all_clients()
        
        data = []
        
        for client in clients:
            data.append(
                {
                    "id" : client.id,
                    "name" : client.name,
                    "email" : client.email
                }
            )
        
        return data
        
    async def find_client(self, client_id:int) -> Clients | str:
        result = await self.client_service.find_client(client_id=client_id)
        
        if result == None:
            return f"Este cliente não esta cadastrado!"
        
        return result
        
    async def delete_client(self, client_id:int) -> None | str:
        
        check = await self.client_service.find_client(client_id=client_id)
        
        if check == None:
            return f"Não existe nenhum cliente de id: {client_id} cadastrado."
        
        await self.client_service.delete_client(client_id)
        
        return
    
    async def update_client(self, client_id:int, name:str = None, email:str = None) -> Clients | str:
        
        check = await self.client_service.find_client(client_id=client_id)
        
        if check == None:
            return f"Não existe nenhum cliente de id: {client_id} cadastrado."
        
        
        if email:
            check = await self.client_service.find_client(email=email)
            
            if check != None:
                return f"O e-mail '{email}' já está sendo usado."
        
        result = await self.client_service.update_client(client_id, name, email)
        
        return result