from typing import Union

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import StudentGet, TeacherGet
from app.services import StudentService, TeacherService
from app.services.auth import get_role_from_access_token, get_user_from_access_token, verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.get(
    "/user/me",
    response_model=Union[StudentGet, TeacherGet],
    response_model_exclude={"password"},
    response_description="Успешный возврат пользователя",
    status_code=status.HTTP_200_OK,
    description="Получить свои данные",
    summary="Получение своих данных",
    # responses={},
)
async def get(
    user: UUID4 = Depends(get_user_from_access_token),
    role: str = Depends(get_role_from_access_token),
    db: AsyncSession = Depends(get_session),
    students_service: StudentService = Depends(),
    teachers_service: TeacherService = Depends(),
):
    if role == "student":
        return await students_service.get(db=db, guid=user)
    elif role == "teacher":
        return await teachers_service.get(db=db, guid=user)
