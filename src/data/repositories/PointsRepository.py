from src.common.Point import Point
from src.data.repositories.Repository import Repository
from src.data.models import Points


class PointsRepository(Repository):

    def GetById(self, identifier):
        session = Repository.SessionFactory()
        record = session.query(Points).filter_by(ID=identifier).first()
        return record

    def List(self):
        session = Repository.SessionFactory()
        records = session.query(Points)
        return [Point(rec.longitude, rec.latitude, rec.value, rec.name, rec.ID) for rec in records]

    def Add(self, item):
        session = Repository.SessionFactory()
        newRecord = Points(ID=item.id, longitude=item.longitude, value=item.value, latitude=item.latitude, name=item.name)
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
        updatedRecord.longitude = item.longitude
        updatedRecord.value = item.value
        updatedRecord.latitude = item.latitude
        updatedRecord.name = item.name
        session.commit()
