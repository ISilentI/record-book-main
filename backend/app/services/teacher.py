from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TeacherCreate, TeacherGet, TeacherPatch
from app.repositories import TeacherRepository


class TeacherService:
    @staticmethod
    async def create(db: AsyncSession, model: TeacherCreate) -> TeacherGet:
        teacher = await TeacherRepository.get_teacher_by_email(db, model.email)
        if teacher is not None:
            raise HTTPException(409, "Преподаватель с таким email уже существует")
        else:
            teacher = await TeacherRepository.create(db, model)
        return TeacherGet.from_orm(teacher)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[TeacherGet]:
        teachers = await TeacherRepository.get_all(db, offset=offset, limit=limit)
        if teachers is None:
            raise HTTPException(404, "Преподаватели не найдены")
        return [TeacherGet.from_orm(t) for t in teachers]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> TeacherGet:
        teacher = await TeacherRepository.get(db, guid)
        if teacher is None:
            raise HTTPException(404, "Преподаватель не найден")
        return TeacherGet.from_orm(teacher)

    @staticmethod
    async def get_teacher_by_email(db: AsyncSession, email: EmailStr) -> TeacherGet:
        teacher = await TeacherRepository.get_teacher_by_email(db, email)
        if teacher is None:
            raise HTTPException(404, "Преподаватель не найден")
        return TeacherGet.from_orm(teacher)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: TeacherCreate) -> TeacherGet:
        teacher = await TeacherRepository.update(db, guid, model)
        if teacher is None:
            raise HTTPException(404, "Преподаватель не найден")
        return TeacherGet.from_orm(teacher)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: TeacherPatch) -> TeacherGet:
        teacher = await TeacherRepository.patch(db, guid, model)
        if teacher is None:
            raise HTTPException(404, "Преподаватель не найден")
        return TeacherGet.from_orm(teacher)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await TeacherRepository.delete(db, guid)
        return Response(status_code=204)
