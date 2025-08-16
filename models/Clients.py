from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.dialects.postgresql import TEXT
from database.base import Base
from sqlalchemy.orm import relationship

class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(255), unique=True, index=True, nullable=False)
    email = Column(VARCHAR(255), unique=True, index=True, nullable=False)
    password = Column(TEXT, nullable=False)
    
    favorites = relationship("Favorites", backref="Favorites", lazy=True)
    
    def __init__(self, name:str, email:str, password:str):
        self.name = name
        self.email = email
        self.password = password