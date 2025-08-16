from fastapi.responses import JSONResponse
from schemas.clients_schemas import ClientResponse, ClientMessage
from controllers.clients_controller import ClientsController
from fastapi import status
from traceback import format_exc
import logging


class ClientsView:
    def __init__(self):
        self.controller = ClientsController()
        
    async def register_client(self, client_name:str, client_email:str, client_password:str) -> JSONResponse:
        try:
            result = await self.controller.registe_client(client_name, client_email, client_password)
            
            if isinstance(result, str):
                return JSONResponse(
                    ClientMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )            
            
            return JSONResponse(
                ClientResponse(
                    id = result.id,
                    name = result.name,
                    email = result.email
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )
            
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                ClientMessage(
                    message="Erro inespeado ao registar cliente, contate o ADM"
                ).model_dump(),
                status_code=status.HTTP_500
            )

    async def find_clients(self, client_id:int = None) -> JSONResponse:
        try:
            if not client_id:
                result = await self.controller.find_all_clients()
                
                return JSONResponse(
                    result,
                    status_code=status.HTTP_200_OK
                )
            
            result = await self.controller.find_client(client_id)
            
            if isinstance(result, str):
                return JSONResponse(
                    ClientMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            return JSONResponse(
                ClientResponse(
                    id = result.id,
                    name = result.name,
                    email = result.email
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )

        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                ClientMessage(
                    message="Erro inespeado ao buscar cliente(s), contate o ADM"
                ).model_dump(),
                status_code=status.HTTP_500
            )
            
    async def delete_client(self, client_id:int) -> JSONResponse:
        try:       
            result = await self.controller.delete_client(client_id)
                
            if isinstance(result, str):
                return JSONResponse(
                    ClientMessage(
                        message=result
                    ),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            return JSONResponse(
                ClientMessage(
                    message="Cliente deletado com sucesso"
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )
        
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                ClientMessage(
                    message="Erro inespeado ao deletar cliente, contate o ADM"
                ).model_dump(),
                status_code=status.HTTP_500
            )
            
    async def update_client(self, client_id:int, name:str = None, email:str = None) -> JSONResponse:
        try:
            if name == None and email == None:
                return JSONResponse(
                    ClientMessage(
                        message="Deve ser fornecido ao menos o nome ou email para atualizar dados do cliente."
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            result = await self.controller.update_client(client_id, name, email)
            
            if isinstance(result, str):
                return JSONResponse(
                    ClientMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            return JSONResponse(
                ClientResponse(
                    id = result.id,
                    name = result.name,
                    email = result.email
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )
            
        except Exception:
            return JSONResponse(
                ClientMessage(
                    message="Erro inespeado ao atualizar cliente, contate o ADM"
                ).model_dump(),
                status_code=status.HTTP_500
            )