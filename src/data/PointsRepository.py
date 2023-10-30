from src.common.Point import Point
from src.data.Repository import Repository
from src.data.models import Points


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
        newRecord = Points(ID=item.id, Longitude=item.longitude, Value=item.value, Latitude=item.latitude, Name=item.name)
        session.add(newRecord)
        session.commit()

    def Delete(self, item):
        session = Repository.SessionFactory()
        deletedRecord = session.query(Points).filter_by(ID=item.id).first()
        session.delete(deletedRecord)
        session.commit()

    def Edit(self, item):
        session = Repository.SessionFactory()
        updatedRecord = session.query(Points).filter_by(ID=item.id).first()
        updatedRecord.Longitude = item.longitude
        updatedRecord.Value = item.value
        updatedRecord.Latitude = item.latitude
        updatedRecord.Name = item.name
        session.commit()
