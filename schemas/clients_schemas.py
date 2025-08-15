from pydantic import BaseModel, EmailStr
from fastapi import Form
from typing import Optional

class ClientRegisterForm(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    @classmethod
    def form(
        self,
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
    ):
        return self(name=name, email=email, password=password)
    
class ClientLoginForm(BaseModel):
    email: EmailStr
    password: str
    
    @classmethod
    def form(
        self,
        email: str = Form(...),
        password: str = Form(...),
    ):
        return self(email=email, password=password)
    
class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    
class ClientToken(BaseModel):
    token: str
    type: str

class ClientMessage(BaseModel):
    message: str
    
class ClientUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None