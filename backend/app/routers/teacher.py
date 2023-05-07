from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import TeacherCreate, TeacherGet, TeacherPatch
from app.services import TeacherService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/teacher",
    response_model=TeacherGet,
    response_model_exclude={"password"},
    response_description="Преподаватель успешно создан",
    status_code=status.HTTP_201_CREATED,
    description="Создать преподавателя и вернуть его",
    summary="Создание преподавателя",
    # responses={},
)
async def create(
    model: TeacherCreate,
    db: AsyncSession = Depends(get_session),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.create(db=db, model=model)


@router.get(
    "/teacher",
    response_model=List[TeacherGet],
    response_model_exclude={"password"},
    response_description="Успешный возврат списка преподавателей",
    status_code=status.HTTP_200_OK,
    description="Получить список всех преподавателей",
    summary="Получение всех преподавателей",
    # responses={},
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/teacher/{id}",
    response_model=TeacherGet,
    response_model_exclude={"password"},
    response_description="Успешный возврат преподавателя",
    status_code=status.HTTP_200_OK,
    description="Получить преподавателя по его id",
    summary="Получение преподавателя по id",
    # responses={},
)
async def get(
    id: UUID4 = Path(None, description="Id преподавателя"),
    db: AsyncSession = Depends(get_session),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.get(db=db, guid=id)


@router.get(
    "/teacher/email/{email}",
    response_model=TeacherGet,
    response_model_exclude={"password"},
    response_description="Успешный возврат преподавателя",
    status_code=status.HTTP_200_OK,
    description="Получить преподавателя по его email",
    summary="Получение преподавателя по email",
    # responses={},
)
async def get(
    email: EmailStr = Path(None, description="Email преподавателя"),
    db: AsyncSession = Depends(get_session),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.get_teacher_by_email(db=db, email=email)


@router.put(
    "/teacher/{id}",
    response_model=TeacherGet,
    response_model_exclude={"password"},
    response_description="Успешное обновление преподавателя",
    status_code=status.HTTP_200_OK,
    description="Изменить преподавателя по его id (полное обновление модели)",
    summary="Изменение преподавателя по id",
    # responses={},
)
async def update(
    model: TeacherCreate,
    id: UUID4 = Path(None, description="Id преподавателя"),
    db: AsyncSession = Depends(get_session),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.update(db=db, guid=id, model=model)


@router.patch(
    "/teacher/{id}",
    response_model=TeacherGet,
    response_model_exclude={"password"},
    response_description="Успешное частичное обновление преподавателя",
    status_code=status.HTTP_200_OK,
    description="Изменить преподавателя по его id (частисно обновление модели)",
    summary="Изменение преподавателя по id (только указанные поля будут изменены)",
    # responses={},
)
async def patch(
    model: TeacherPatch,
    id: UUID4 = Path(None, description="Id преподавателя"),
    db: AsyncSession = Depends(get_session),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/teacher/{id}",
    response_description="Успешное удаление преподавателя",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить преподавателя по его id",
    summary="Удаление преподавателя по id",
    # responses={},
)
async def delete(
    id: UUID4 = Path(None, description="Id преподавателя"),
    db: AsyncSession = Depends(get_session),
    teachers_service: TeacherService = Depends(),
):
    return await teachers_service.delete(db=db, guid=id)
