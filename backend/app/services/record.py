from __future__ import annotations

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RecordCreate, RecordGet
from app.repositories import RecordRepository


class RecordService:
    @staticmethod
    async def create(db: AsyncSession, guid: UUID4, tguid: UUID4, yguid: UUID4, model: RecordCreate) -> RecordGet:
        record = await RecordRepository.create(db, guid, tguid, yguid, model)
        if record is None:
            raise HTTPException(409, "Оценка с таким названием уже существует")
        return RecordGet.from_orm(record)

    @staticmethod
    async def get_by_student(db: AsyncSession, guid: UUID4) -> list[RecordGet]:
        student = await RecordRepository.get_by_student(db, guid)
        if student is None:
            raise HTTPException(404, "Оценка не найдена")
        return [RecordGet.from_orm(r) for r in student.records]
