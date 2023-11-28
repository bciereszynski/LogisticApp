from src.common.Courier import Courier
from src.data.repositories.Repository import Repository
from src.data.models import Couriers


class CouriersRepository(Repository):

    def GetById(self, identifier):
        session = Repository.SessionFactory()
        record = session.query(Couriers).filter_by(ID=identifier).first()
        return record

    def List(self):
        session = Repository.SessionFactory()
        records = session.query(Couriers)
        return [Courier(rec.name, rec.surname, rec.email, rec.color, rec.ID) for rec in records]

    def Add(self, item):
        session = Repository.SessionFactory()
        newRecord = Couriers(ID=item.id, name = item.name, surname = item.surname, email = item.email, color = item.color)
        session.add(newRecord)
        session.commit()

    def Delete(self, item):
        session = Repository.SessionFactory()
        deletedRecord = session.query(Couriers).filter_by(ID=item.id).first()
        session.delete(deletedRecord)
        session.commit()

    def Edit(self, item):
        session = Repository.SessionFactory()
        updatedRecord = session.query(Couriers).filter_by(ID=item.id).first()
        updatedRecord.name = item.name
        updatedRecord.surname = item.surname
        updatedRecord.email = item.email
        updatedRecord.color = item.color
        session.commit()
