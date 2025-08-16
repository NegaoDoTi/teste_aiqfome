from schemas.clients_schemas import ClientToken, ClientMessage
from fastapi.responses import JSONResponse
from fastapi import status
from controllers.login_controller import LoginController
from traceback import format_exc
import logging

class LoginView():
    """Classe responsável pela apresentação visual do login
    """
    
    def __init__(self):
        self.controller = LoginController()
        
    async def login_client(self, email:str, password:str) -> JSONResponse:
        """Efeuta o login do cliente utiliando JWT

        Args:
            email (str): email do cliente
            password (str): senha do cliente

        Returns:
            JSONResponse: resposta em formato json
        """
        
        try:
            result = await self.controller.login_client(email, password)
            
            if isinstance(result, str):
                return JSONResponse(
                    ClientMessage(
                        message=result
                    ).model_dump(),
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
                
            return JSONResponse(
                ClientToken(
                    token=result["token"],
                    type=result["type"]
                ).model_dump(),
                status_code=status.HTTP_200_OK
            )
            
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                ClientMessage(
                    message="Erro inesprado ao efetuar login, contate o ADM!"
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )