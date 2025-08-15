from database.connection import async_session
from models.Clients import Clients
from sqlalchemy.future import select
from sqlalchemy import delete, update

class ClientsService:
    async def create_client(self, name:str, email:str, hash_password:str) -> Clients:
        async with async_session() as session:
            client = Clients(name=name, email=email, password=hash_password)
            
            session.add(client)
            
            await session.commit()
            await session.refresh(client)
            
            await session.close()
            
        return client    
    
    async def find_client(self, client_id:int = None, email:str = "") -> Clients | None:
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
        async with async_session() as session:
            
            query = delete(Clients).where(Clients.id == client_id)
            
            await session.execute(query)
            
            await session.commit()
            
            await session.close()
            
        return
    
    async def update_client(self, client_id:int, name:str = None, email:str = None) -> Clients:
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
            
            