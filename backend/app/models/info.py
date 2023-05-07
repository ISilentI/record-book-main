from typing import Optional

from pydantic import UUID4, BaseModel, Field

from app.models.utils import optional


class InfoBase(BaseModel):
    group: Optional[str] = Field(None, description="Учебная группа пользователя")
    course: Optional[int] = Field(None, description="Курс обучения пользователя")
    departament: Optional[str] = Field(None, description="Кафедра пользователя")
    position: Optional[str] = Field(None, description="Должность пользователя")


class InfoCreate(InfoBase):
    pass


class InfoGet(InfoBase):
    guid: UUID4 = Field(description="Уникальный идентификатор информации о пользователе")

    class Config:
        orm_mode = True


@optional
class InfoPatch(InfoCreate):
    pass
