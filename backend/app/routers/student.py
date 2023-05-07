from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import StudentCreate, StudentGet, StudentPatch
from app.services import StudentService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/student",
    response_model=StudentGet,
    response_model_exclude={"password"},
    response_description="Студент успешно создан",
    status_code=status.HTTP_201_CREATED,
    description="Создать студента и вернуть его",
    summary="Создание студента",
    # responses={},
)
async def create(
    model: StudentCreate,
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
):
    return await students_service.create(db=db, model=model)


@router.get(
    "/student",
    response_model=List[StudentGet],
    response_model_exclude={"password"},
    response_description="Успешный возврат списка студентов",
    status_code=status.HTTP_200_OK,
    description="Получить список всех студентов",
    summary="Получение всех студентов",
    # responses={},
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    students_service: StudentService = Depends(),
):
    return await students_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/student/{id}",
    response_model=StudentGet,
    response_model_exclude={"password"},
    response_description="Успешный возврат студента",
    status_code=status.HTTP_200_OK,
    description="Получить студента по его id",
    summary="Получение студента по id",
    # responses={},
)
async def get(
    id: UUID4 = Path(None, description="Id студента"),
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
):
    return await students_service.get(db=db, guid=id)


@router.get(
    "/student/email/{email}",
    response_model=StudentGet,
    response_model_exclude={"password"},
    response_description="Успешный возврат студента",
    status_code=status.HTTP_200_OK,
    description="Получить студента по его email",
    summary="Получение студента по email",
    # responses={},
)
async def get(
    email: EmailStr = Path(None, description="Email студента"),
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
):
    return await students_service.get_student_by_email(db=db, email=email)


@router.put(
    "/student/{id}",
    response_model=StudentGet,
    response_model_exclude={"password"},
    response_description="Успешное обновление студента",
    status_code=status.HTTP_200_OK,
    description="Изменить студента по его id (полное обновление модели)",
    summary="Изменение студента по id",
    # responses={},
)
async def update(
    model: StudentCreate,
    id: UUID4 = Path(None, description="Id студента"),
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
):
    return await students_service.update(db=db, guid=id, model=model)


@router.patch(
    "/student/{id}",
    response_model=StudentGet,
    response_model_exclude={"password"},
    response_description="Успешное частичное обновление студента",
    status_code=status.HTTP_200_OK,
    description="Изменить студента по его id (частисно обновление модели)",
    summary="Изменение студента по id (только указанные поля будут изменены)",
    # responses={},
)
async def patch(
    model: StudentPatch,
    id: UUID4 = Path(None, description="Id студента"),
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
):
    return await students_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/student/{id}",
    response_description="Успешное удаление студента",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить студента по его id",
    summary="Удаление студента по id",
    # responses={},
)
async def delete(
    id: UUID4 = Path(None, description="Id студента"),
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
):
    return await students_service.delete(db=db, guid=id)
