from database.connection import async_session
from models.Clients import Clients
from sqlalchemy.future import select
from sqlalchemy import delete, update

class ClientsService:
    """Responsavel por servir dados da tablea clientes
    """
    
    async def create_client(self, name:str, email:str, hash_password:str) -> Clients:
        """Cria um cliente

        Args:
            name (str): nome do cliente
            email (str): email do cliente
            hash_password (str): senha do cliente criptografada

        Returns:
            Clients
        """
        async with async_session() as session:
            client = Clients(name=name, email=email, password=hash_password)
            
            session.add(client)
            
            await session.commit()
            await session.refresh(client)
            
            await session.close()
            
        return client    
    
    async def find_client(self, client_id:int = None, email:str = "") -> Clients | None:
        """Busca um cliente

        Args:
            client_id (int, optional): Pode buscar pelo id. Defaults to None.
            email (str, optional): Ou pode buscar pelo email. Defaults to "".

        Returns:
            Clients | None: retorna None se nao se o cliente nao estiver registrado no DB
        """
        
        async with async_session() as session:
            if client_id:
                query = select(Clients).where(Clients.id == client_id)
                
            if email:    
                query = select(Clients).where(Clients.email == email)
            
            response = await session.execute(query)
            
            try:
                client = response.scalars().one()
            except:
                client = None

            await session.close()
            
        return client
    
    async def find_all_clients(self) -> list[Clients]:
        """Busca todos o clientes

        Returns:
            list[Clients]: retorna uma lista de clientes
        """
        async with async_session() as session:
            query = select(Clients)
            
            response = await session.execute(query)
            
            try:
                results = response.scalars().all()
            except:
                results = []
            
            await session.close()
            
        clients = []
        
        for result in results:
            clients.append(result)
            
        return clients
                
    async def delete_client(self, client_id:int) -> None:
        """Deleta um cliente no banco de dados

        Args:
            client_id (int): id do cliente
        """
        
        async with async_session() as session:
            
            query = delete(Clients).where(Clients.id == client_id)
            
            await session.execute(query)
            
            await session.commit()
            
            await session.close()
            
        return
    
    async def update_client(self, client_id:int, name:str = None, email:str = None) -> Clients:
        """Altera dados de um cliente no banco de dados 

        Args:
            client_id (int): id do cliente
            name (str, optional): nome do cliente e opcional. Defaults to None.
            email (str, optional): email do cliente e opcional. Defaults to None.

        Returns:
            Clients
        """
        
        async with async_session() as session:
            client = await session.get(Clients, client_id)
            
            if name:
                client.name = name
                
            if email:
                client.email = email
                
            await session.commit()
            
            await session.refresh(client)
            
            await session.close()
            
        return client
            
            