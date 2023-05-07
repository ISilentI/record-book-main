from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field

from app.models.record import RecordGet
from app.models.utils import optional


class StudentBase(BaseModel):
    email: EmailStr = Field(description="Email адрес студента")
    first_name: str = Field(description="Имя студента")
    last_name: str = Field(description="Фамилия студента")
    middle_name: Optional[str] = Field(None, description="Отчество студента(при наличии)")
    role: str = Field("student", description="Роль студента")
    group: str = Field(description="Группа студента")
    course: int = Field(description="Курс студента")


class StudentCreate(StudentBase):
    password: str = Field(description="Пароль студента")


class StudentGet(StudentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор студента")
    is_deleted: bool = Field(False, description="Активен ли пользователь")
    records: Optional[list[RecordGet]] = Field(None, description="Список оценок студента(при наличии)")
    created_at: datetime = Field(description="Время создания студента")
    updated_at: datetime = Field(description="Время последнего обновления студента")

    class Config:
        orm_mode = True


@optional
class StudentPatch(StudentCreate):
    pass
