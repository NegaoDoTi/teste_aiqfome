from database.connection import async_session
from models.Favorites import Favorites
from sqlalchemy.future import select
from sqlalchemy import delete, update

class FavoritesService():
    """Responsavel por servir dados da tabela favorites
    """
    
    async def create_favorite(self, 
            product_id:int, 
            client_id:int, 
            title:str, 
            image:str,
            price:float,
            review:float
    ) -> Favorites:
        """Cria um favorito e vincula ele a um cliente

        Args:
            product_id (int): id do produto na api fakestore
            client_id (int): id do cliente
            title (str): titulo do produto
            image (str): image do produto
            price (float): preço do produto
            review (float): nota do produto

        Returns:
            Favorites
        """
        
        
        async with async_session() as session:
            favorite = Favorites(
                product_id=product_id,
                client_id=client_id,
                title=title,
                image=image,
                price=price,
                review=review
            )
            
            session.add(favorite)
            
            await session.commit()
            await session.refresh(favorite)
            
            await session.close()
            
        return favorite    
    
    async def find_favorite(self, favorite_id:int, client_id:int) -> Favorites | None:
        """Busca um favorito de um cliente

        Args:
            favorite_id (int): id do favorito
            client_id (int): id do cliente

        Returns:
            Favorites | None: retorna None de não encontrar
        """
        
        async with async_session() as session:
            
            query = select(Favorites).where(
                Favorites.id == favorite_id and Favorites.client_id == client_id
            )
                
            response = await session.execute(query)
            
            try:
                favorite = response.scalars().one()
            except:
                favorite = None

            await session.close()
            
        return favorite
    
    async def find_product(self, product_id:int, client_id:int) -> Favorites | None:
        """Busca um favorito pelo id do produto e pelo id do cliente para verificar se ja foi cadastrado

        Args:
            product_id (int): id do produto
            client_id (int): id do cliente

        Returns:
            Favorites | None: retorna None se nao encontrar
        """
        
        async with async_session() as session:
            query = select(Favorites).where(
                Favorites.product_id == product_id and Favorites.client_id == client_id
            )
                
            response = await session.execute(query)
            
            try:
                favorite = response.scalars().one()
            except:
                favorite = None

            await session.close()
            
        return favorite
    
    
    async def find_all_favorites(self, client_id:int) -> list[Favorites]:
        """Busca todos os favoritos de 1 cliente

        Args:
            client_id (int): id do cliente

        Returns:
            list[Favorites]: lista de favoritos
        """
        
        async with async_session() as session:
            query = select(Favorites).where(
                Favorites.client_id == client_id
            )
                
            response = await session.execute(query)
            
            try:
                results = response.scalars().all()
            except:
                results = None

            await session.close()
            
        favorites = []
        
        for result in results:
            favorites.append(result)
        
        return favorites
    
    async def delete_favorite(self, favorite_id:int) -> None:
        """Deleta 1 favorito

        Args:
            favorite_id (int): id do favorito
        """
        
        async with async_session() as session:
            
            query = delete(Favorites).where(Favorites.id == favorite_id)
            
            await session.execute(query)
            
            await session.commit()
            
            await session.close()
            
        return
    
    async def update_favorite(self, 
        favorite_id:int, 
        product_id:str, 
        title:str,
        image:str,
        price:float,
        review:float
    ) -> Favorites:
        """Alterar os dados de um favorito de um cliente

        Args:
            product_id (int): id do produto na api fakestore
            client_id (int): id do cliente
            title (str): titulo do produto
            image (str): image do produto
            price (float): preço do produto
            review (float): nota do produto


        Returns:
            Favorites
        """
        
        
        async with async_session() as session:
            favorite = await session.get(Favorites, favorite_id)
            
            favorite.product_id = product_id
            
            favorite.title = title
            
            favorite.image = image
            
            favorite.price = price
            
            favorite.review = review
                
            await session.commit()
            
            await session.refresh(favorite)
            
            await session.close()
            
        return favorite