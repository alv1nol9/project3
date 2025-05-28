from sqlalchemy import Column, Integer, String
from . import Base

class Customer(Base):
    __tablename__ = "customers"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    rentals = [] 
    from sqlalchemy.orm import relationship
    rentals = relationship("Rental", back_populates="customer")