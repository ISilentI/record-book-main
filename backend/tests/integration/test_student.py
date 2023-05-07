import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_student, create_random_student


class TestRecord:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()
        assert "is_deleted" in body.keys()
        assert "created_at" in body.keys()
        assert "updated_at" in body.keys()

    @pytest.mark.asyncio
    async def test_get_students(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_student(client=client, headers=headers)

        response = await client.get("/student", headers=headers)
        assert response.status_code == 200

        students = response.json()
        assert len(students) == 10

    @pytest.mark.asyncio
    async def test_get_students_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_student(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/student", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_students_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_student(client=client, headers=headers)
        response = await client.get("/student", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_student(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        student = await create_base_student(client=client, headers=headers)
        response = await client.get(f"/student/{student['guid']}", headers=headers)
        assert response.status_code == 200

        student = response.json()
        assert student["email"] == test_models.STUDENT_CREATE_EMAIL
        assert student["first_name"] == test_models.STUDENT_CREATE_FIRST_NAME
        assert student["last_name"] == test_models.STUDENT_CREATE_LAST_NAME
        assert student["middle_name"] == test_models.STUDENT_CREATE_MIDDLE_NAME
        assert student["role"] == test_models.STUDENT_CREATE_ROLE
        assert student["group"] == test_models.STUDENT_CREATE_GROUP
        assert student["course"] == test_models.STUDENT_CREATE_COURSE
        await self.check_system(student)

    @pytest.mark.asyncio
    async def test_get_student_by_email(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        student = await create_base_student(client=client, headers=headers)
        response = await client.get(f"/student/email/{student['email']}", headers=headers)
        assert response.status_code == 200

        student = response.json()
        assert student["email"] == test_models.STUDENT_CREATE_EMAIL
        assert student["first_name"] == test_models.STUDENT_CREATE_FIRST_NAME
        assert student["last_name"] == test_models.STUDENT_CREATE_LAST_NAME
        assert student["middle_name"] == test_models.STUDENT_CREATE_MIDDLE_NAME
        assert student["role"] == test_models.STUDENT_CREATE_ROLE
        assert student["group"] == test_models.STUDENT_CREATE_GROUP
        assert student["course"] == test_models.STUDENT_CREATE_COURSE
        await self.check_system(student)

    @pytest.mark.asyncio
    async def test_post_student(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/student", headers=headers, json=jsonable_encoder(test_models.STUDENT_CREATE))
        assert response.status_code == 201

        student = response.json()
        assert student["email"] == test_models.STUDENT_CREATE_EMAIL
        assert student["first_name"] == test_models.STUDENT_CREATE_FIRST_NAME
        assert student["last_name"] == test_models.STUDENT_CREATE_LAST_NAME
        assert student["middle_name"] == test_models.STUDENT_CREATE_MIDDLE_NAME
        assert student["role"] == test_models.STUDENT_CREATE_ROLE
        assert student["group"] == test_models.STUDENT_CREATE_GROUP
        assert student["course"] == test_models.STUDENT_CREATE_COURSE
        await self.check_system(student)

    @pytest.mark.asyncio
    async def test_put_student(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        student = await create_base_student(client=client, headers=headers)
        response = await client.put(
            f"/student/{student['guid']}", headers=headers, json=jsonable_encoder(test_models.STUDENT_PUT)
        )
        assert response.status_code == 200

        student = response.json()
        assert student["email"] == test_models.STUDENT_PUT_EMAIL
        assert student["first_name"] == test_models.STUDENT_PUT_FIRST_NAME
        assert student["last_name"] == test_models.STUDENT_PUT_LAST_NAME
        assert student["middle_name"] == test_models.STUDENT_PUT_MIDDLE_NAME
        assert student["role"] == test_models.STUDENT_PUT_ROLE
        assert student["group"] == test_models.STUDENT_PUT_GROUP
        assert student["course"] == test_models.STUDENT_PUT_COURSE
        await self.check_system(student)

    @pytest.mark.asyncio
    async def test_delete_student(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        student = await create_base_student(client=client, headers=headers)
        response = await client.delete(f"/student/{student['guid']}", headers=headers)
        assert response.status_code == 204

        response = await client.get(f"/student/{student['guid']}", headers=headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_patch_student(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        student = await create_base_student(client=client, headers=headers)
        response = await client.patch(
            f"/student/{student['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.STUDENT_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        student = response.json()
        assert student["email"] == test_models.STUDENT_PATCH_EMAIL
        await self.check_system(student)
