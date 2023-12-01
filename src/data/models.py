from sqlalchemy import Column, Integer, String, Uuid, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Points(Base):
    __tablename__ = "points"

    ID = Column(Uuid, primary_key=True)
    longitude = Column(Numeric(15, 10))
    latitude = Column(Numeric(15, 10))
    value = Column(Integer)
    name = Column(String(50))
    isCentral = Column(Boolean, default=False)


class Couriers(Base):
    __tablename__ = "couriers"
    ID = Column(Uuid, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    color = Column(String(10))
