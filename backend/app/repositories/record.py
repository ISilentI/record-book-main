from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.tables import Record, Student
from app.models import RecordCreate
from app.repositories.student import StudentRepository
from app.repositories.teacher import TeacherRepository
from app.repositories.year import YearRepository


class RecordRepository:
    @staticmethod
    async def create(db: AsyncSession, guid: UUID4, tguid: UUID4, yguid: UUID4, model: RecordCreate) -> Record:
        student = await StudentRepository.get(db, guid)
        teacher = await TeacherRepository.get(db, tguid)
        year = await YearRepository.get(db, yguid)
        record = Record(**model.dict())
        record.student = student
        record.teacher = teacher
        record.year = year
        db.add(record)
        await db.commit()
        return record

    @staticmethod
    async def get_by_student(db: AsyncSession, guid: UUID4) -> Student:
        res = await db.execute(select(Student).where(Student.guid == guid).limit(1))
        return res.scalar()
