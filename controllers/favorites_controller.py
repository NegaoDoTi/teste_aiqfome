from models.Favorites import Favorites
from services.favorites_service import FavoritesService
from repositories.fakestore_repositore import FakeStoreRepositore


class FavoritesController():
    """Responsavel por controllar a rota favoritos
    """
    
    def __init__(self):
        self.favorites_service = FavoritesService()
        self.fakestore_repo = FakeStoreRepositore()
        
    async def register_favorite(self, product_id:int, client_id:int) -> Favorites | str:
        """Registar um produto no favorito de um cliente no banco de dados

        Args:
            product_id (int): id do produto na api fakestore
            client_id (int): id cliente

        Returns:
            Favorites | str: retorna string caso ocorra algo de errado
        """
        
        check = await self.favorites_service.find_product(product_id, client_id)
        
        if check != None:
            return f"O produto de id: {product_id}, já foi cadastrado nos favoritos"
        
        product_data = await self.fakestore_repo.find_product(product_id)
        
        if product_data == None:
            return f"O producto de id: {product_id}, não existe"
        
        favorite =  await self.favorites_service.create_favorite(
            product_id=product_data["id"],
            client_id=client_id,
            title=product_data["title"],
            image=product_data["image"],
            price=product_data["price"],
            review=product_data["rating"]["rate"]
        )
        
        return favorite
    
    async def find_all_favorites(self, client_id:int) -> list[dict]:
        """Busca todos os produtos favoritos de 1 cliente

        Args:
            client_id (int): id cliente

        Returns:
            list[dict]: lista de Favoritos
        """
        
        favorites = await self.favorites_service.find_all_favorites(client_id)
        
        data = []
        
        for favorite in favorites:
            
            data.append(
                {
                    "id": favorite.id,
                    "product_id": favorite.product_id,
                    "client_id": favorite.client_id,
                    "title": favorite.title,
                    "image": favorite.image,
                    "price" : favorite.price,
                    "review": favorite.review
                }
            )
        
        return data
        
    async def find_favorite(self, favorite_id:int, client_id:int) -> Favorites | str:
        """Busca um produto favorito de um cliente

        Args:
            favorite_id (int): id do favorito
            client_id (int): id do cliente

        Returns:
            Favorites | str: retorna string caso ocorra algo de errado
        """
        
        favorite = await self.favorites_service.find_favorite(favorite_id, client_id)
        
        if favorite == None:
            return f"Você não tem um favorito cadastrado de id:{favorite_id}"
        
        return favorite
    
    async def delete_favorite(self, favorite_id:str, client_id:int) -> None | str:
        """Deleta um produto favorito de um cliente

        Args:
            favorite_id (str): id do favorito
            client_id (int): id do cliente

        Returns:
            None | str: retorna string caso ocorra algo de errado
        """
        
        check = await self.favorites_service.find_favorite(favorite_id, client_id)
        
        if check == None:
            return f"Você não tem nenhum favorito de id: {favorite_id}"
        
        await self.favorites_service.delete_favorite(favorite_id)
        
        return
    
    async def update_favorite(self, favorite_id:int, product_id:int, client_id:int) -> Favorites | str:
        """Atualiza um produto favorito de um cliente

        Args:
            favorite_id (int): id do favorito
            product_id (int): id do produto na fakestore
            client_id (int): id do cliente

        Returns:
            Favorites | str: retorna string caso ocorra algo de errado
        """
        
        check = await self.favorites_service.find_product(product_id, client_id)
        
        if check != None:
            return f"O produto de id: {product_id}, já está cadastrado no seu favoritos"
        
        check_favorite = await self.favorites_service.find_favorite(favorite_id, client_id)
        
        if check_favorite == None:
            return f"Você não tem um favorito de id: {favorite_id}, cadastrado!"
        
        product_data = await self.fakestore_repo.find_product(product_id)
        
        if product_data == None:
            return f"O producto de id: {product_id}, não existe"
        
        favorite = await self.favorites_service.update_favorite(
            favorite_id=favorite_id,
            product_id=product_data["id"],
            title=product_data["title"],
            image=product_data["image"],
            price=product_data["price"],
            review=product_data["rating"]["rate"]
        )
        
        return favorite
        