import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_teacher, create_random_teacher


class TestRecord:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()
        assert "is_deleted" in body.keys()
        assert "created_at" in body.keys()
        assert "updated_at" in body.keys()

    @pytest.mark.asyncio
    async def test_get_teachers(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_teacher(client=client, headers=headers)

        response = await client.get("/teacher", headers=headers)
        assert response.status_code == 200

        teachers = response.json()
        assert len(teachers) == 10

    @pytest.mark.asyncio
    async def test_get_teachers_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_teacher(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/teacher", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_teachers_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_teacher(client=client, headers=headers)
        response = await client.get("/teacher", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_teacher(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        teacher = await create_base_teacher(client=client, headers=headers)
        response = await client.get(f"/teacher/{teacher['guid']}", headers=headers)
        assert response.status_code == 200

        teacher = response.json()
        assert teacher["email"] == test_models.TEACHER_CREATE_EMAIL
        assert teacher["first_name"] == test_models.TEACHER_CREATE_FIRST_NAME
        assert teacher["last_name"] == test_models.TEACHER_CREATE_LAST_NAME
        assert teacher["middle_name"] == test_models.TEACHER_CREATE_MIDDLE_NAME
        assert teacher["role"] == test_models.TEACHER_CREATE_ROLE
        assert teacher["departament"] == test_models.TEACHER_CREATE_DEPARTAMENT
        assert teacher["position"] == test_models.TEACHER_CREATE_POSITION
        await self.check_system(teacher)

    @pytest.mark.asyncio
    async def test_get_teacher_by_email(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        teacher = await create_base_teacher(client=client, headers=headers)
        response = await client.get(f"/teacher/email/{teacher['email']}", headers=headers)
        assert response.status_code == 200

        teacher = response.json()
        assert teacher["email"] == test_models.TEACHER_CREATE_EMAIL
        assert teacher["first_name"] == test_models.TEACHER_CREATE_FIRST_NAME
        assert teacher["last_name"] == test_models.TEACHER_CREATE_LAST_NAME
        assert teacher["middle_name"] == test_models.TEACHER_CREATE_MIDDLE_NAME
        assert teacher["role"] == test_models.TEACHER_CREATE_ROLE
        assert teacher["departament"] == test_models.TEACHER_CREATE_DEPARTAMENT
        assert teacher["position"] == test_models.TEACHER_CREATE_POSITION
        await self.check_system(teacher)

    @pytest.mark.asyncio
    async def test_post_teacher(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/teacher", headers=headers, json=jsonable_encoder(test_models.TEACHER_CREATE))
        assert response.status_code == 201

        teacher = response.json()
        assert teacher["email"] == test_models.TEACHER_CREATE_EMAIL
        assert teacher["first_name"] == test_models.TEACHER_CREATE_FIRST_NAME
        assert teacher["last_name"] == test_models.TEACHER_CREATE_LAST_NAME
        assert teacher["middle_name"] == test_models.TEACHER_CREATE_MIDDLE_NAME
        assert teacher["role"] == test_models.TEACHER_CREATE_ROLE
        assert teacher["departament"] == test_models.TEACHER_CREATE_DEPARTAMENT
        assert teacher["position"] == test_models.TEACHER_CREATE_POSITION
        await self.check_system(teacher)

    @pytest.mark.asyncio
    async def test_put_teacher(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        teacher = await create_base_teacher(client=client, headers=headers)
        response = await client.put(
            f"/teacher/{teacher['guid']}", headers=headers, json=jsonable_encoder(test_models.TEACHER_PUT)
        )
        assert response.status_code == 200

        teacher = response.json()
        assert teacher["email"] == test_models.TEACHER_PUT_EMAIL
        assert teacher["first_name"] == test_models.TEACHER_PUT_FIRST_NAME
        assert teacher["last_name"] == test_models.TEACHER_PUT_LAST_NAME
        assert teacher["middle_name"] == test_models.TEACHER_PUT_MIDDLE_NAME
        assert teacher["role"] == test_models.TEACHER_PUT_ROLE
        assert teacher["departament"] == test_models.TEACHER_PUT_DEPARTAMENT
        assert teacher["position"] == test_models.TEACHER_PUT_POSITION
        await self.check_system(teacher)

    @pytest.mark.asyncio
    async def test_delete_teacher(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        teacher = await create_base_teacher(client=client, headers=headers)
        response = await client.delete(f"/teacher/{teacher['guid']}", headers=headers)
        assert response.status_code == 204

        response = await client.get(f"/teacher/{teacher['guid']}", headers=headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_patch_teacher(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        teacher = await create_base_teacher(client=client, headers=headers)
        response = await client.patch(
            f"/teacher/{teacher['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.TEACHER_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        teacher = response.json()
        assert teacher["email"] == test_models.TEACHER_PATCH_EMAIL
        await self.check_system(teacher)
