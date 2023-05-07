from typing import List

from fastapi import HTTPException
from pydantic import UUID4, EmailStr
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Student
from app.models import StudentCreate, StudentPatch


class StudentRepository:
    @staticmethod
    async def create(db: AsyncSession, model: StudentCreate) -> Student:
        student = Student(**model.dict())
        db.add(student)
        await db.commit()
        await db.refresh(student)
        return student

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Student]:
        res = await db.execute(select(Student).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Student:
        res = await db.execute(select(Student).where(Student.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def get_student_by_email(db: AsyncSession, email: EmailStr) -> Student:
        res = await db.execute(select(Student).where(Student.email == email).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: StudentCreate) -> Student:
        student = await StudentRepository.get(db, guid)

        if student is None:
            raise HTTPException(404, "Студент не найден")

        from app.services.auth import crypt_password

        model.password = crypt_password(model.password)

        await db.execute(update(Student).where(Student.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(student)

        return student

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: StudentPatch) -> Student:
        student = await StudentRepository.get(db, guid)

        if student is None:
            raise HTTPException(404, "Студент не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Student).where(Student.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(student)

        return student

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(Student).where(Student.guid == guid))
        await db.commit()
