from pydantic import BaseModel


class FavoriteProductRegister(BaseModel):
    product_id: int

class FavoriteUpdate(BaseModel):
    product_id: int
    
class FavoritesMessage(BaseModel):
    message:str
    
class FavoritesResponse(BaseModel):
    id:int
    product_id:int
    client_id:int
    title:str
    image:str
    price:float
    review:float