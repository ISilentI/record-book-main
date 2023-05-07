from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StudentCreate, StudentGet, StudentPatch
from app.repositories import StudentRepository


class StudentService:
    @staticmethod
    async def create(db: AsyncSession, model: StudentCreate) -> StudentGet:
        student = await StudentRepository.get_student_by_email(db, model.email)
        if student is not None:
            raise HTTPException(409, "Студент с таким email уже существует")
        else:
            student = await StudentRepository.create(db, model)
        return StudentGet.from_orm(student)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[StudentGet]:
        students = await StudentRepository.get_all(db, offset=offset, limit=limit)
        if students is None:
            raise HTTPException(404, "Студенты не найдены")
        return [StudentGet.from_orm(s) for s in students]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> StudentGet:
        student = await StudentRepository.get(db, guid)
        if student is None:
            raise HTTPException(404, "Студент не найден")
        return StudentGet.from_orm(student)

    @staticmethod
    async def get_student_by_email(db: AsyncSession, email: EmailStr) -> StudentGet:
        student = await StudentRepository.get_student_by_email(db, email)
        if student is None:
            raise HTTPException(404, "Студент не найден")
        return StudentGet.from_orm(student)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: StudentCreate) -> StudentGet:
        student = await StudentRepository.update(db, guid, model)
        if student is None:
            raise HTTPException(404, "Студент не найден")
        return StudentGet.from_orm(student)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: StudentPatch) -> StudentGet:
        student = await StudentRepository.patch(db, guid, model)
        if student is None:
            raise HTTPException(404, "Студент не найден")
        return StudentGet.from_orm(student)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await StudentRepository.delete(db, guid)
        return Response(status_code=204)
