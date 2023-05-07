from app.models.enums import BaseEnum


class Role(str, BaseEnum):
    STUDENT = "student"
    TEACHER = "teacher"
