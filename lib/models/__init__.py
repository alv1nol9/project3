from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .car import Car
from .customer import Customer
from .rental import Rental