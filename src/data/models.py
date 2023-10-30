from sqlalchemy import Column, Integer, String, Uuid, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Points(Base):
    __tablename__ = "Points"

    ID = Column(Uuid, primary_key=True)
    Longitude = Column(Numeric(15, 10))
    Latitude = Column(Numeric(15, 10))
    Value = Column(Integer)
    Name = Column(String(50))
