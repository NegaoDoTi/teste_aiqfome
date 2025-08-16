from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from schemas.favorites_schemas import FavoriteProductRegister, FavoriteUpdate
from views.favorites_view import FavoritesView

#Rota favoritos
favorites_route = APIRouter()

@favorites_route.get("/favoritos", response_class=JSONResponse)
async def find_favorite(request: Request):
    return await FavoritesView().find_favorites(request)
    
@favorites_route.get("/favoritos/{favorite_id}", response_class=JSONResponse)
async def find_favorites(favorite_id:int, request: Request):
    return await FavoritesView().find_favorites(request, favorite_id)
    
@favorites_route.post("/favoritos", response_class=JSONResponse)
async def register_favorite(product: FavoriteProductRegister, request: Request):
    return await FavoritesView().register_favorite(request, product.product_id)

@favorites_route.delete("/favoritos/{favorite_id}", response_class=JSONResponse)
async def delete_favorite(favorite_id:int, request:Request):
    return await FavoritesView().delete_favorite(request, favorite_id)

@favorites_route.put("/favoritos/{favorite_id}", response_class=JSONResponse)
async def update_favorite(product: FavoriteUpdate, favorite_id:int, request:Request):
    return await FavoritesView().update_favorite(request, favorite_id, product.product_id)