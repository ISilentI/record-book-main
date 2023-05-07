import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_year, create_random_year


class TestRecord:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()

    @pytest.mark.asyncio
    async def test_get_years(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_year(client=client, headers=headers)

        response = await client.get("/year", headers=headers)
        assert response.status_code == 200

        years = response.json()
        assert len(years) == 10

    @pytest.mark.asyncio
    async def test_get_years_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_year(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/year", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_years_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_year(client=client, headers=headers)
        response = await client.get("/year", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_year(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        year = await create_base_year(client=client, headers=headers)
        response = await client.get(f"/year/{year['guid']}", headers=headers)
        assert response.status_code == 200

        year = response.json()
        assert year["name"] == test_models.YEAR_CREATE_NAME
        await self.check_system(year)

    @pytest.mark.asyncio
    async def test_post_year(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/year", headers=headers, json=jsonable_encoder(test_models.YEAR_CREATE))
        assert response.status_code == 201

        year = response.json()
        assert year["name"] == test_models.YEAR_CREATE_NAME
        await self.check_system(year)

    @pytest.mark.asyncio
    async def test_put_year(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        year = await create_base_year(client=client, headers=headers)
        response = await client.put(
            f"/year/{year['guid']}", headers=headers, json=jsonable_encoder(test_models.YEAR_PUT)
        )
        assert response.status_code == 200

        year = response.json()
        assert year["name"] == test_models.YEAR_PUT_NAME
        await self.check_system(year)

    @pytest.mark.asyncio
    async def test_delete_year(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        year = await create_base_year(client=client, headers=headers)
        response = await client.delete(f"/year/{year['guid']}", headers=headers)
        assert response.status_code == 204

        response = await client.get(f"/year/{year['guid']}", headers=headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_patch_year(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        year = await create_base_year(client=client, headers=headers)
        response = await client.patch(
            f"/year/{year['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.YEAR_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        year = response.json()
        assert year["name"] == test_models.YEAR_PATCH_NAME
        await self.check_system(year)
