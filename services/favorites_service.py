from database.connection import async_session
from models.Favorites import Favorites
from sqlalchemy.future import select
from sqlalchemy import delete, update

class FavoritesService():
    async def create_favorite(self, 
            product_id:int, 
            client_id:int, 
            title:str, 
            image:str,
            price:float,
            review:float
    ) -> Favorites:
        
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