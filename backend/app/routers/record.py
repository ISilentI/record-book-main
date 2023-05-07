from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import RecordCreate, RecordGet
from app.models.enums import Role
from app.services import RecordService
from app.services.auth import get_role_from_access_token, get_user_from_access_token, verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/student/{id}/record",
    response_model=RecordGet,
    response_description="Оценка успешно создана",
    status_code=status.HTTP_201_CREATED,
    description="Создать оценку студенту и вернуть её",
    summary="Создание оценки студенту",
    # responses={},
)
async def create(
    id: UUID4 = Path(description="ID студента"),
    year: UUID4 = Query(description="ID года обучения"),
    model: RecordCreate = Body(description="Модель оценки"),
    teacher: UUID4 = Depends(get_user_from_access_token),
    role: str = Depends(get_role_from_access_token),
    db: AsyncSession = Depends(get_session),
    records_service: RecordService = Depends(),
):
    if role == Role.TEACHER:
        return await records_service.create(db=db, guid=id, tguid=teacher, yguid=year, model=model)
    raise HTTPException(status_code=403, detail="У вас нет прав на выполнение этого действия")


@router.get(
    "/student/{id}/record",
    response_model=list[RecordGet],
    response_description="Успешный возврат списка оценок",
    status_code=status.HTTP_200_OK,
    description="Получить список оценок студента",
    summary="Получение списка оценок студента",
    # responses={},
)
async def get(
    id: UUID4 = Path(description="ID студента"),
    db: AsyncSession = Depends(get_session),
    role: str = Depends(get_role_from_access_token),
    records_service: RecordService = Depends(),
):
    if role == Role.TEACHER:
        return await records_service.get_by_student(db=db, guid=id)
    raise HTTPException(status_code=403, detail="У вас нет прав на выполнение этого действия")


@router.get(
    "/student/record/my",
    response_model=list[RecordGet],
    response_description="Успешный возврат списка оценок",
    status_code=status.HTTP_200_OK,
    description="Получить список своих оценок",
    summary="Получение списка своих оценок",
    # responses={},
)
async def get_my(
    db: AsyncSession = Depends(get_session),
    student: UUID4 = Depends(get_user_from_access_token),
    role: str = Depends(get_role_from_access_token),
    records_service: RecordService = Depends(),
):
    if role == Role.STUDENT:
        return await records_service.get_by_student(db=db, guid=student)
    raise HTTPException(status_code=403, detail="У вас нет прав на выполнение этого действия")
