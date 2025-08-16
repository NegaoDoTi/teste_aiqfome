from httpx import AsyncClient

class FakeStoreRepositore:
    """Repo da api fakestore
    """
    
    def __init__(self):
        self.products_url = "https://fakestoreapi.com/products/"
    
    
    async def find_product(self, product_id:int) -> dict | None:
        """Busca um produto na api para verificar se ele é valido

        Args:
            product_id (int): id do produto

        Returns:
            dict | None: Retorna None se ocorrer algo de errado
        """
        
        async with AsyncClient() as client_http:
            response = await client_http.get(url=f"{self.products_url}/{product_id}")
            
            if response.status_code == 200:
                product = response.json()
                
                return product
            
            return None