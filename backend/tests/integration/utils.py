import random
import secrets

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models


async def create_base_record(client: AsyncClient, headers: dict, student: dict, year: dict) -> dict:
    response = await client.post(
        f"/student/{student['guid']}/record?year={year['guid']}",
        headers=headers,
        json=jsonable_encoder(test_models.RECORD_CREATE),
    )
    return response.json()


async def create_base_teacher(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/teacher", headers=headers, json=jsonable_encoder(test_models.TEACHER_CREATE))
    return response.json()


async def create_random_teacher(client: AsyncClient, headers: dict) -> dict:
    email = secrets.token_hex(10) + "@test.com"
    first_name = secrets.token_hex(10)
    last_name = secrets.token_hex(10)
    middle_name = secrets.token_hex(10)
    role = "teacher"
    departament = secrets.token_hex(10)
    position = secrets.token_hex(10)
    password = secrets.token_hex(10)

    body = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "role": role,
        "departament": departament,
        "position": position,
        "password": password,
    }

    response = await client.post("/teacher", headers=headers, json=jsonable_encoder(body))
    return response.json()


async def create_base_student(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/student", headers=headers, json=jsonable_encoder(test_models.STUDENT_CREATE))
    return response.json()


async def create_random_student(client: AsyncClient, headers: dict) -> dict:
    email = secrets.token_hex(10) + "@test.com"
    first_name = secrets.token_hex(10)
    last_name = secrets.token_hex(10)
    middle_name = secrets.token_hex(10)
    role = "student"
    group = secrets.token_hex(10)
    course = random.randint(1, 6)
    password = secrets.token_hex(10)

    body = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "role": role,
        "group": group,
        "course": course,
        "password": password,
    }

    response = await client.post("/student", headers=headers, json=jsonable_encoder(body))
    return response.json()


async def create_base_year(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/year", headers=headers, json=jsonable_encoder(test_models.YEAR_CREATE))
    return response.json()


async def create_random_year(client: AsyncClient, headers: dict) -> dict:
    name = secrets.token_hex(10)

    body = {
        "name": name,
    }

    response = await client.post("/year", headers=headers, json=jsonable_encoder(body))
    return response.json()
