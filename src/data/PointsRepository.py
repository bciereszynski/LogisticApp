import uuid

from sqlalchemy import String, Column, Integer
import sqlalchemy

from src.common.Point import Point
from src.data.Repository import Repository
from src.data.models import Points


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

class PointsRepository(Repository):

    def GetById(self, identifier):
        session = Repository.SessionFactory()
        record = session.query(Points).filter_by(ID=identifier).first()
        return record

    def List(self):
        session = Repository.SessionFactory()
        records = session.query(Points)
        return [Point(rec.Longitude, rec.Latitude, rec.Value, rec.Name, rec.ID) for rec in records]

    def Add(self, item):
        session = Repository.SessionFactory()
        newRecord = Points(ID=item.id, Longitude=item.longitude, Value=item.value, Latitude=item.Latitude, Name=item.value)
        session.add(newRecord)
        session.commit()

    def Delete(self, item):
        session = Repository.SessionFactory()
        deletedRecord = session.query(Points).filter_by(ID=item.ID).first()
        session.delete(deletedRecord)
        session.commit()

    def Edit(self, item):
        session = Repository.SessionFactory()
        updatedRecord = session.query(Points).filter_by(ID=item.ID).first()
        updatedRecord.Longitude = item.longitude
        updatedRecord.Value = item.value
        updatedRecord.Latitude = item.latitude
        updatedRecord.Name = item.name
        session.commit()
