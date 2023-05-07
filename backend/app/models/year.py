from pydantic import UUID4, BaseModel, Field

from app.models.utils import optional


class YearBase(BaseModel):
    name: str = Field(description="Название года обучения")


class YearCreate(YearBase):
    pass


class YearGet(YearBase):
    guid: UUID4 = Field(description="Уникальный идентификатор года обучения")

    class Config:
        orm_mode = True


@optional
class YearPatch(YearCreate):
    pass
