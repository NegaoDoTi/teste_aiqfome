from database.base import Base
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    external_id = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    title = Column(TEXT, nullable=False)
    image = Column(TEXT, nullable=False)
    price = Column(Float, nullable=False)
    review = Column(Float, nullable=False)
    
    def __init__(self, external_id:int, client_id:str, title:str, image:str, price:float, review:float):
        self.external_id = external_id
        self.client_id = client_id
        self.title = title
        self.image = image
        self.price = price
        self.review = review