from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field

from app.models.utils import optional


class TeacherBase(BaseModel):
    email: EmailStr = Field(description="Email адрес преподавателя")
    first_name: str = Field(description="Имя преподавателя")
    last_name: str = Field(description="Фамилия преподавателя")
    middle_name: Optional[str] = Field(None, description="Отчество преподавателя(при наличии)")
    role: str = Field("student", description="Роль преподавателя")
    departament: str = Field(description="Кафедра преподавателя")
    position: str = Field(description="Должность преподавателя")


class TeacherCreate(TeacherBase):
    password: str = Field(description="Пароль преподавателя")


class TeacherGet(TeacherBase):
    guid: UUID4 = Field(description="Уникальный идентификатор преподавателя")
    is_deleted: bool = Field(False, description="Активен ли пользователь")
    created_at: datetime = Field(description="Время создания преподавателя")
    updated_at: datetime = Field(description="Время последнего обновления преподавателя")

    class Config:
        orm_mode = True


@optional
class TeacherPatch(TeacherCreate):
    pass
