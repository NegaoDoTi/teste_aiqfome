from pydantic import BaseModel


class ProductRegister(BaseModel):
    id: int
    title: str
    image: str
    price: str
    review: float