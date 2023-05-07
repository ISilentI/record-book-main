from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import config
from app.models.exceptions import add_exception_handlers, catch_unhandled_exceptions
from app.routers.auth import router as auth_router
from app.routers.record import router as record_router
from app.routers.student import router as student_router
from app.routers.teacher import router as teacher_router
from app.routers.user import router as user_router
from app.routers.year import router as year_router

tags_metadata = [
    {"name": "auth", "description": "Авторизация"},
    {"name": "users", "description": "Работа с пользователями"},
    {"name": "students", "description": "Работа со студентами"},
    {"name": "teachers", "description": "Работа с преподавателями"},
    {"name": "years", "description": "Работа с годами обучения"},
    {"name": "records", "description": "Работа с оценками"},
]

app = FastAPI(
    debug=config.DEBUG,
    openapi_tags=tags_metadata,
    openapi_url=f"{config.BACKEND_PREFIX}/openapi.json",
    title=config.BACKEND_TTILE,
    description=config.BACKEND_DESCRIPTION,
)

app.middleware("http")(catch_unhandled_exceptions)
add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["users"])
app.include_router(student_router, tags=["students"])
app.include_router(teacher_router, tags=["teachers"])
app.include_router(year_router, tags=["years"])
app.include_router(record_router, tags=["records"])

"commit"