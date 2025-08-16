from httpx import AsyncClient

class FakeStoreRepositore:
    def __init__(self):
        self.products_url = "https://fakestoreapi.com/products/"
    
    
    async def find_product(self, product_id:int) -> dict | None:
        async with AsyncClient() as client_http:
            response = await client_http.get(url=f"{self.products_url}/{product_id}")
            
            if response.status_code == 200:
                product = response.json()
                
                return product
            
            return None