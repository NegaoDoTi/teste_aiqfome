from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.clients_schemas import ClientRegisterForm, ClientUpdate
from views.clients_view import ClientsView

clients_route = APIRouter()

@clients_route.get("/clientes/{client_id}", response_class=JSONResponse)
async def find_client(client_id:int):
    return await ClientsView().find_clients(client_id)

@clients_route.get("/clientes", response_class=JSONResponse)
async def find_clients():
    return await ClientsView().find_clients()
    
@clients_route.post("/clientes", response_class=JSONResponse)
async def register_client(form: ClientRegisterForm = Depends(ClientRegisterForm.form)):
    return await ClientsView().register_client(form.name, form.email, form.password)
    
@clients_route.delete("/clientes/{client_id}", response_class=JSONResponse)
async def delete_client(client_id:int):
    return await ClientsView().delete_client(client_id)

@clients_route.put("/clientes/{client_id}")
async def update_client(client_id:int, client_data:ClientUpdate):
    return await ClientsView().update_client(client_id, name=client_data.name, email=client_data.email)