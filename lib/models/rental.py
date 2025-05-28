from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from . import Base

class Rental(Base):
    __tablename__ = "rentals"

    id          = Column(Integer, primary_key=True, index=True)
    car_id      = Column(Integer, ForeignKey("cars.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    start_date  = Column(Date, nullable=False)
    end_date    = Column(Date, nullable=True)

    car      = relationship("Car", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")
    