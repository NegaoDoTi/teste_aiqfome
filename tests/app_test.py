from fastapi.testclient import TestClient
from app import app

#Testes da API

cliente = {
    "name" : "Nome de teste",
    "email" : "teste@teste@gmail",
    "password" : "teste123456",
}
cliente_id = None

token = ""

test_client = TestClient(app)

def test_register_client():
    
    response = test_client.post("/clientes", data=cliente)
    
    assert response.status_code == 201
    assert "id" in response.json()
    
    cliente_id = response.json()["id"]
    
    assert response.json()["name"] == cliente["name"]
    assert response.json()["email"] == cliente["email"]
    
def test_fail_register_cliente():
    
    response = test_client.post("/clientes", data={cliente["name"]})
    
    assert response.status_code == 422
    
def test_find_clients():
    
    
    response = test_client.get("/clientes")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    
    response_2 = test_client.get(f"/clientes/{cliente_id}")
    
    assert response_2.status_code == 200
    assert response_2.json() == {"name" : cliente["name"], "email" : cliente["email"]}

def test_fail_find_client():
    
    response = test_client.get("/clientes/999")
    
    assert response.status_code == 400
    assert response.json() == {"message" : "Este cliente não esta cadastrado!"}
    
def test_update_client():
    
    cliente["name"] = "Nome de teste2"
    cliente["email"] = "teste2@teste.com"
    
    response = test_client.put(f"/clientes/{cliente_id}", data={"name" : cliente["name"], "email" : cliente["email"]})
    
    assert response.status_code == 200
    assert response.json() == {"id" : cliente_id, "name" : cliente["name"], "email" : cliente["email"]}
    
    
def test_fail_update_client():
    
    response = test_client.put(f"/clientes/{cliente_id}", data={})
    
    assert response.status_code == 400
    assert response.json() == {"message" : "Deve ser fornecido ao menos o nome ou email para atualizar dados do cliente."}
    
def test_login_client():

    response = test_client.post("/login", data={"email" : cliente["email"], "password" : cliente["password"]})
    
    assert response.status_code == 200
    assert isinstance(response.json()["token"], str)
    assert response.json()["type"] == "Bearer"
    
def test_fail_login_cliet():
    
    response = test_client.post("/login", data={"email" : "wgagwqatyaw158@gmail.com", "password" : "wgaw7g4awg8463"})
    
    assert response.status_code == 401
    assert response.json() == {"message" : "Cliente não cadastrado"}

    response = test_client.post("/login", data={"email" : cliente["email"], "password" : "wgaw7g4awg8463"})
    
    assert response.status_code == 401
    assert response.json() == {"message" : "Email ou senha incorretos!"}


favorito_id = None
favorito = {}

produto = {
    "id" : 1
}

def test_favorite_register():
    response = test_client.post("/favoritos", data={"product_id" : produto["id"]})
    
    assert response.status_code == 201
    
    favorito_id = response.json()["id"]
    
    assert response.json()["product_id"] == produto["id"]
    
    favorito = response.json()

def test_fail_favorite_register():
    false_product = 999
    
    response = test_client.post("/favoritos", data={"product_id" : false_product})
    
    assert response.status_code == 400
    assert response.json() == {"message" : f"O producto de id: {false_product}, não existe"}
    
def test_find_favorite():
    response = test_client.get(f"/favoritos/{favorito_id}")
    
    assert response.status_code == 200
    assert response.json() == favorito

def test_fail_find_favorite():
    false_favorite = 9985
    
    response = test_client.get(f"/favoritos/{false_favorite}")
    
    assert response.status_code == 400
    assert response.json() == {"message" : f"Você não tem um favorito cadastrado de id:{false_favorite}"}
    
def test_update_favorite():
    
    response = test_client.put(f"/favoritos/{favorito_id}", data={"product_id": 2})
    
    assert response.status_code == 200
    assert response.json()["product_id"] == 2
    favorito = response.json()
    
def test_fail_update_favorite():
    
    result = test_client.post("/favoritos", data={"product_id" : 3})
    test_client.post("/favoritos", data={"product_id" : 4})
    
    response = test_client.put(f'/favoritos/{result["id"]}', data={"product" : 4})
    
    assert response.status_code == 400
    assert response.json() == {"message" : "O produto de id: 4, já está cadastrado no seu favoritos"}
    
    response_2 = test_client.put(f'/favoritos/985', data={"product" : 3})
    
    assert response_2.status_code == 400
    assert response_2.json() == {"message" : "Você não tem um favorito de id: 985, cadastrado!"}
    
    response_3 = test_client.put(f"/favoritos/{result['id']}", data={"product_id" : 9999})
    
    assert response_3.status_code == 400
    assert response_3.json() == {"message" : "O producto de id: 9999, não existe"}

def test_delete_favorite():

    response = test_client.delete(f"/favoritos/{favorito_id}")
    
    assert response.status_code == 200
    assert response.json() == {"message" : "Favorito deletado com sucesso"}
    
def test_fail_delete_favorite():
    
    response = test_client.delete("/favoritos/9832")

    assert response.status_code == 400
    assert response.json() == {"message" : "Você não tem nenhum favorito de id: 9832"}

def test_delete_client():
    
    response = test_client.delete(f"/clientes/{cliente_id}")
    
    assert response.status_code == 200
    assert response.json() == {"message" : "Cliente deletado com sucesso"}
    
def test_fail_delete_client():
    
    response = test_client.delete("/clientes/999")
    
    assert response.status_code == 400
    assert response.json() == {"message" : f"Não existe nenhum cliente de id: {cliente_id} cadastrado."}