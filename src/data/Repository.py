from sqlalchemy import create_engine, String, Column, Integer
import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = create_engine("mariadb+pymysql://root:@localhost:3306/logisticdb")
factory = sessionmaker(bind=engine)
session = factory()

# insert
# new_rec = Employees(Name="xd", Age="xd")
# session.add(new_rec)
# session.commit()

# read
# for instance in session.query(Employees):
#     print("Name: ", instance.Name)
#     print("Age: ", instance.Age)
#     print("---------")

# update
# updated_rec = session.query(Orders).filter_by(SOME_ID_COLUMN="SOME_ID_VALUE").first()
# updated_rec.ShipCountry = "USA"
# session.commit()
#
# delete
# deleted_rec = session.query(Orders).filter_by(SOME_ID_COLUMN="SOME_ID_VALUE").first()
# session.delete(deleted_rec)
# session.commit()
