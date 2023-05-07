from datetime import datetime

from pydantic import UUID4, BaseModel, Field

from app.models.teacher import TeacherGet
from app.models.utils import optional
from app.models.year import YearGet


class RecordBase(BaseModel):
    name: str = Field(description="Название предмета")
    term: int = Field(description="Семестр")
    mark: str = Field(description="Оценка")
    exam_date: datetime = Field(description="Дата экзамена")
    exam_type: str = Field(description="Тип экзамена")


class RecordCreate(RecordBase):
    pass


class RecordGet(RecordBase):
    guid: UUID4 = Field(description="Уникальный идентификатор оценки")
    year: YearGet = Field(description="Год обучения")
    teacher: TeacherGet = Field(description="Преподаватель")

    class Config:
        orm_mode = True


@optional
class RecordPatch(RecordCreate):
    pass
