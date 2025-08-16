from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.clients_schemas import ClientLoginForm
from views.login_view import LoginView

#Rota login
login_route = APIRouter()

@login_route.post("/login", response_class=JSONResponse)
async def login_client(form: ClientLoginForm = Depends(ClientLoginForm.form)):
    return await LoginView().login_client(form.email, form.password)