from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import YearCreate, YearGet, YearPatch
from app.repositories import YearRepository


class YearService:
    @staticmethod
    async def create(db: AsyncSession, model: YearCreate) -> YearGet:
        year = await YearRepository.create(db, model)
        if year is None:
            raise HTTPException(409, "Год обучения с таким названием уже существует")
        return YearGet.from_orm(year)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[YearGet]:
        years = await YearRepository.get_all(db, offset=offset, limit=limit)
        if years is None:
            raise HTTPException(404, "Года обучения не найдены")
        return [YearGet.from_orm(y) for y in years]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> YearGet:
        year = await YearRepository.get(db, guid)
        if year is None:
            raise HTTPException(404, "Год обучения не найден")
        return YearGet.from_orm(year)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: YearCreate) -> YearGet:
        year = await YearRepository.update(db, guid, model)
        if year is None:
            raise HTTPException(404, "Год обучения не найден")
        return YearGet.from_orm(year)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: YearPatch) -> YearGet:
        year = await YearRepository.patch(db, guid, model)
        if year is None:
            raise HTTPException(404, "Год обучения не найден")
        return YearGet.from_orm(year)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await YearRepository.delete(db, guid)
        return Response(status_code=204)
