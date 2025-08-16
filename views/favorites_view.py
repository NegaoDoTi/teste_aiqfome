from fastapi.responses import JSONResponse
from fastapi import status, Request
from schemas.favorites_schemas import FavoritesMessage, FavoritesResponse
from validators.validate_login import verify_jwt_login
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from controllers.favorites_controller import FavoritesController
from traceback import format_exc
import logging

class FavoritesView():
    """Classe responsável pela apresentação visual do favoritos
    """
    
    def __init__(self):
        self.controller = FavoritesController()
        
    async def register_favorite(self, request:Request, product_id:int) -> JSONResponse:
        """Registar um favorito

        Args:
            request (Request): requisição http
            product_id (int): id do produto na fakestore

        Returns:
            JSONResponse: resposta em formato json
        """
        
        try:
            try:
                token = request.headers["Authorization"].split("Bearer ")[-1]
            except Exception:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token de autorização deve ser fornecido! No header da requisição"
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                payload = await verify_jwt_login(token)
            except ExpiredSignatureError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token expirado faça login novamente!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
            except InvalidTokenError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token invalido!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
                
            result = await self.controller.register_favorite(product_id,  payload["client_id"])
            
            if isinstance(result, str):
                return JSONResponse(
                    FavoritesMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            return JSONResponse(
                FavoritesResponse(
                    id=result.id,
                    product_id=result.product_id,
                    client_id=result.client_id,
                    title=result.title,
                    image=result.image,
                    price=result.price,
                    review=result.review
                ).model_dump(),
                status_code=status.HTTP_201_CREATED
            )
            
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                FavoritesMessage(
                    message="Erro inesperado ao registar Produto Favorito, contate o ADM!"
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    async def find_favorites(self, request:Request, favorite_id:int = None) -> JSONResponse:
        """Busca um favorito ou todos os favoritos de um cliente

        Args:
            request (Request): requisição http
            favorite_id (int, optional): id do favorito e opcional. Defaults to None.

        Returns:
            JSONResponse: resposta em formato json
        """
        
        try:
            try:
                token = request.headers["Authorization"].split("Bearer ")[-1]
            except Exception:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token de autorização deve ser fornecido! No header da requisição"
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                payload = await verify_jwt_login(token)
            except ExpiredSignatureError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token expirado faça login novamente!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
            except InvalidTokenError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token invalido!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
            
            if not favorite_id:
            
                result = await self.controller.find_all_favorites(payload["client_id"])
            
                return JSONResponse(
                    result,
                    status_code=status.HTTP_200_OK
                )
            
            result = await self.controller.find_favorite(favorite_id, payload["client_id"])
            
            if isinstance(result, str):
                return JSONResponse(
                    FavoritesMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            return JSONResponse(
                FavoritesResponse(
                    id=result.id,
                    product_id=result.product_id,
                    client_id=result.client_id,
                    title=result.title,
                    image=result.image,
                    price=result.price,
                    review=result.review
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )
                
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                FavoritesMessage(
                    message="Erro inesperado ao buscar favorito(s), contate o ADM!"
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    async def delete_favorite(self, request:Request, favorite_id:int) -> JSONResponse:
        """Deleta um favorito de um cliente

        Args:
            request (Request): requisição http
            favorite_id (int): id do favorito

        Returns:
            JSONResponse: resposta em formato json
        """
        
        try:
            try:
                token = request.headers["Authorization"].split("Bearer ")[-1]
            except Exception:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token de autorização deve ser fornecido! No header da requisição"
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                payload = await verify_jwt_login(token)
            except ExpiredSignatureError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token expirado faça login novamente!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
            except InvalidTokenError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token invalido!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
                
            result = await self.controller.delete_favorite(favorite_id, payload["client_id"])
            
            if isinstance(result, str):
                return JSONResponse(
                    FavoritesMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            return JSONResponse(
                FavoritesMessage(
                    message="Favorito deletado com sucesso"
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                FavoritesMessage(
                    message="Erro inesperado ao deletar favorito, contate o ADM!"
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    async def update_favorite(self, request:Request, favorite_id:int, product_id:int) -> JSONResponse:
        """Altera o dados de 1 favorito de um cliente

        Args:
            request (Request): requisição http
            favorite_id (int): id do favorito
            product_id (int): id do produto na fakestore

        Returns:
            JSONResponse: resposta em formato json
        """
        
        try:
            try:
                token = request.headers["Authorization"].split("Bearer ")[-1]
            except Exception:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token de autorização deve ser fornecido! No header da requisição"
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                payload = await verify_jwt_login(token)
            except ExpiredSignatureError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token expirado faça login novamente!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
            except InvalidTokenError:
                return JSONResponse(
                    FavoritesMessage(
                        message="Token invalido!"  
                    ).model_dump(), 
                    status.HTTP_401_UNAUTHORIZED
                )
                
            result = await self.controller.update_favorite(favorite_id, product_id, payload["client_id"])
            
            if isinstance(result, str):
                return JSONResponse(
                    FavoritesMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            return JSONResponse(
                FavoritesResponse(
                    id=result.id,
                    product_id=result.product_id,
                    client_id=result.client_id,
                    title=result.title,
                    image=result.image,
                    price=result.price,
                    review=result.review
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )
            
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                FavoritesMessage(
                    message="Erro inesperado ao alterar favorito, contate o ADM!"
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )