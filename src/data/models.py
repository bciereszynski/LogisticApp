from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Employees(Base):
    __tablename__ = "Employees"

    Name = Column(String(50), primary_key=True)
    Age = Column(Integer)

class Employers(Base):
    __tablename__ = "Employers"

    Name = Column(String(50), primary_key=True)
    Age = Column(Integer)
