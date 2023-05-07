import traceback
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from loguru import logger
from pydantic import UUID4, BaseModel
from starlette.responses import JSONResponse

from app.config import config


async def catch_unhandled_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        error = {
            "message": get_endpoint_message(request),
            "errors": [Message(message="Отказано в обработке из-за неизвестной ошибки на сервере")],
        }
        if not config.DEBUG:
            logger.info(traceback.format_exc())
            return JSONResponse(status_code=500, content=jsonable_encoder(error))
        else:
            raise


class Message(BaseModel):
    id: Optional[UUID4]
    message: str

    def __hash__(self):
        return hash((self.id, self.message))


endpoint_message = {
    ("POST", "/api/signin"): "Ошибка входа в систему",
    ("POST", "/api/signup"): "Ошибка регистрации в системе",
    ("GET", "/api/user/me"): "Ошибка получения пользователя",
    ("POST", "/api/student"): "Ошибка создания студента",
    ("GET", "/api/student"): "Ошибка получения всех студентов",
    ("GET", "/api/student/{id}"): "Ошибка получения студента по id",
    ("GET", "/api/student/email/{email}"): "Ошибка получения студента по email",
    ("PUT", "/api/student/{id}"): "Ошибка изменения студента по id",
    ("PATCH", "/api/student/{id}"): "Ошибка частичного изменения студента по id",
    ("DELETE", "/api/student/{id}"): "Ошибка удаления студента по id",
    ("POST", "/api/teacher"): "Ошибка создания преподавателя",
    ("GET", "/api/teacher"): "Ошибка получения всех преподавателей",
    ("GET", "/api/teacher/{id}"): "Ошибка получения преподавателя по id",
    ("GET", "/api/teacher/email/{email}"): "Ошибка получения преподавателя по email",
    ("PUT", "/api/teacher/{id}"): "Ошибка изменения преподавателя по id",
    ("PATCH", "/api/teacher/{id}"): "Ошибка частичного изменения преподавателя по id",
    ("DELETE", "/api/teacher/{id}"): "Ошибка удаления преподавателя по id",
    ("POST", "/api/year"): "Ошибка создания года обучения",
    ("GET", "/api/year"): "Ошибка получения всех годов обучения",
    ("GET", "/api/year/{id}"): "Ошибка получения года обучения по id",
    ("PUT", "/api/year/{id}"): "Ошибка изменения года обучения по id",
    ("PATCH", "/api/year/{id}"): "Ошибка частичного изменения года обучения по id",
    ("DELETE", "/api/year/{id}"): "Ошибка удаления года обучения по id",
    ("POST", "/api/student/{id}/record"): "Ошибка создания оценки студенту",
    ("GET", "/api/student/{id}/record"): "Ошибка получения оценок студента",
    ("GET", "/api/student/record"): "Ошибка получения своих оценок",
}


def get_endpoint_message(request: Request):
    method, path = request.scope["method"], request.scope["path"]
    for path_parameter, value in request.scope["path_params"].items():
        path = path.replace(value, "{" + path_parameter + "}")
    return endpoint_message.get((method, path))


class ValidationUtils:
    @staticmethod
    def validate_type_error(error):
        field = error["loc"][-1]
        type_ = error["type"].split(".")[-1]
        msg = error["msg"]
        return f'Поле "{field}" Имеет неверный тип данных. Укажите "{type_}" ({msg})'

    @staticmethod
    def validate_const(error):
        field = error["loc"][-1]
        value = error["ctx"]["given"]
        allowed_values = error["ctx"]["permitted"]
        return (
            f'Поле "{field}" имеет некорректное значение, Вы указали  "{value}". Возможные значения: {allowed_values}'
        )

    @staticmethod
    def validate_invalid_discriminator(error):
        allowed_values = error["ctx"]["allowed_values"]
        discriminator_value = error["ctx"]["discriminator_key"]
        user_value = error["ctx"]["discriminator_value"]

        return (
            f'Поле "{discriminator_value}" является обязательным. Вы указали "{user_value}".'
            f"Возможные значения {allowed_values}"
        )

    @staticmethod
    def validate_missing_discriminator(error):
        discriminator_value = error["ctx"]["discriminator_key"]

        return f'Поле "{discriminator_value}" является обязательным.'

    @staticmethod
    def validate_missing(error):
        field = error["loc"][-1]
        return f"Поле {field} является обязательным"


templates_function = {
    "missing": ValidationUtils.validate_missing,
    "const": ValidationUtils.validate_const,
    "": ValidationUtils.validate_type_error,
    "invalid_discriminator": ValidationUtils.validate_invalid_discriminator,
    "missing_discriminator": ValidationUtils.validate_missing_discriminator,
}


class ValidationHandler:
    @classmethod
    async def _build_final_error(cls, request: Request, errors: List[Message]):
        return {"message": get_endpoint_message(request), "errors": list(set(errors))}

    @classmethod
    async def _build_message(cls, type_: str, error: dict):
        try:
            if type_ in templates_function.keys():
                return templates_function[type_](error)
            else:
                return templates_function[""](error)
        except KeyError:
            return error["msg"]

    @classmethod
    async def validation_handler(cls, request: Request, exc):
        errors = []
        for error in exc.errors():
            type_ = error["type"].split(".")[-1]
            message = await cls._build_message(type_, error)
            errors.append(Message(message=message))

        error = await cls._build_final_error(request, errors)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error))


async def logging_handler(request: Request, exc: HTTPException):
    error = {"message": get_endpoint_message(request), "errors": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(error))


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, ValidationHandler.validation_handler)
    app.add_exception_handler(HTTPException, logging_handler)
