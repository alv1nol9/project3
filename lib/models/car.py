from sqlalchemy import Column, Integer, String, Boolean
from . import Base


class Car(Base):
    __tablename__ = "cars"

    id        = Column(Integer, primary_key=True, index=True)
    make      = Column(String, nullable=False)
    model     = Column(String, nullable=False)
    year      = Column(Integer, nullable=False)
    available = Column(Boolean, default=True, nullable=False)

    rentals = []
    from sqlalchemy.orm import relationship
    rentals = relationship("Rental", back_populates="car")
