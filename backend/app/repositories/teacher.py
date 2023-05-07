from typing import List

from fastapi import HTTPException
from pydantic import UUID4, EmailStr
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Teacher
from app.models import TeacherCreate, TeacherPatch


class TeacherRepository:
    @staticmethod
    async def create(db: AsyncSession, model: TeacherCreate) -> Teacher:
        teacher = Teacher(**model.dict(exclude={"info"}))
        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)
        return teacher

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Teacher]:
        res = await db.execute(select(Teacher).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Teacher:
        res = await db.execute(select(Teacher).where(Teacher.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def get_teacher_by_email(db: AsyncSession, email: EmailStr) -> Teacher:
        res = await db.execute(select(Teacher).where(Teacher.email == email).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: TeacherCreate) -> Teacher:
        teacher = await TeacherRepository.get(db, guid)

        if teacher is None:
            raise HTTPException(404, "Преподаватель не найден")

        from app.services.auth import crypt_password

        model.password = crypt_password(model.password)

        await db.execute(update(Teacher).where(Teacher.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(teacher)

        return teacher

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: TeacherPatch) -> Teacher:
        teacher = await TeacherRepository.get(db, guid)

        if teacher is None:
            raise HTTPException(404, "Преподаватель не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Teacher).where(Teacher.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(teacher)

        return teacher

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(Teacher).where(Teacher.guid == guid))
        await db.commit()
