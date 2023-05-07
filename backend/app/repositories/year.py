from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Year
from app.models import YearCreate, YearPatch


class YearRepository:
    @staticmethod
    async def create(db: AsyncSession, model: YearCreate) -> Year:
        year = Year(**model.dict(exclude_unset=True))
        db.add(year)
        await db.commit()
        await db.refresh(year)
        return year

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[Year]:
        res = await db.execute(select(Year).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Year:
        res = await db.execute(select(Year).where(Year.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: YearCreate) -> Year:
        year = await YearRepository.get(db, guid)

        if year is None:
            raise HTTPException(404, "Год обучения не найден")

        await db.execute(update(Year).where(Year.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(year)

        return year

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: YearPatch) -> Year:
        year = await YearRepository.get(db, guid)

        if year is None:
            raise HTTPException(404, "Год обучения не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Year).where(Year.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(year)

        return year

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(Year).where(Year.guid == guid))
        await db.commit()
