from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import YearCreate, YearGet, YearPatch
from app.services import YearService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/year",
    response_model=YearGet,
    response_description="Год обучения успешно создан",
    status_code=status.HTTP_201_CREATED,
    description="Создать год обучения и вернуть его",
    summary="Создание года обучения",
    # responses={},
)
async def create(
    model: YearCreate,
    db: AsyncSession = Depends(get_session),
    years_service: YearService = Depends(),
):
    return await years_service.create(db=db, model=model)


@router.get(
    "/year",
    response_model=list[YearGet],
    response_description="Успешный возврат списка годов обучения",
    status_code=status.HTTP_200_OK,
    description="Получить список всех годов обучения",
    summary="Получение всех годов обучения",
    # responses={},
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    years_service: YearService = Depends(),
):
    return await years_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/year/{id}",
    response_model=YearGet,
    response_description="Успешный возврат года обучения",
    status_code=status.HTTP_200_OK,
    description="Получить год обучения по его id",
    summary="Получение года обучения по id",
    # responses={},
)
async def get(
    id: UUID4 = Path(None, description="Id года обучения"),
    db: AsyncSession = Depends(get_session),
    years_service: YearService = Depends(),
):
    return await years_service.get(db=db, guid=id)


@router.put(
    "/year/{id}",
    response_model=YearGet,
    response_description="Успешное обновление года обучения",
    status_code=status.HTTP_200_OK,
    description="Изменить год обучения по его id (полное обновление модели)",
    summary="Изменение года обучения по id",
    # responses={},
)
async def update(
    model: YearCreate,
    id: UUID4 = Path(None, description="Id года обучения"),
    db: AsyncSession = Depends(get_session),
    years_service: YearService = Depends(),
):
    return await years_service.update(db=db, guid=id, model=model)


@router.patch(
    "/year/{id}",
    response_model=YearGet,
    response_description="Успешное частичное обновление года обучения",
    status_code=status.HTTP_200_OK,
    description="Изменить год обучения по его id (частисно обновление модели)",
    summary="Изменение года обучения по id (только указанные поля будут изменены)",
    # responses={},
)
async def patch(
    model: YearPatch,
    id: UUID4 = Path(None, description="Id года обучения"),
    db: AsyncSession = Depends(get_session),
    years_service: YearService = Depends(),
):
    return await years_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/year/{id}",
    response_description="Успешное удаление года обучения",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить год обучения по его id",
    summary="Удаление года обучения по id",
    # responses={},
)
async def delete(
    id: UUID4 = Path(None, description="Id года обучения"),
    db: AsyncSession = Depends(get_session),
    years_service: YearService = Depends(),
):
    return await years_service.delete(db=db, guid=id)
