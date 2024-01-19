from sqlalchemy import Column, Integer, String, Uuid, Numeric, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship

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
    routeId = Column(Uuid, ForeignKey("routes.ID"), nullable=True)


class Couriers(Base):
    __tablename__ = "couriers"
    ID = Column(Uuid, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    color = Column(String(10))


class Routes(Base):
    __tablename__ = "routes"

    ID = Column(Uuid, primary_key=True)
    courierId = Column(Uuid, ForeignKey("couriers.ID"))
    courier = Relationship("Couriers")
    routes = Relationship("Points", backref='routes')
