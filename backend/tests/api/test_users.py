from urllib import response

from httpx import AsyncClient

from app.core.config import settings
from tests.utils import get_jwt_header


class TestGetUsers:
    async def test_superuser_get_users(self, client: AsyncClient, create_superuser, default_password):
        user = await create_superuser()
        jwt_header = get_jwt_header(user)

        resp = await client.get(settings.API_PATH + "/users", headers=jwt_header)

        assert resp.status_code == 200, resp.text
        assert len(resp.json()) >= 1
        assert resp.json()["items"][0]["id"]
        assert resp.json()["items"][0]["email"]
        assert resp.json()["items"][0]["is_active"]

    async def test_unauthorized(self, client: AsyncClient):
        resp = await client.get(settings.API_PATH + "/users")
        assert resp.status_code == 401, resp.text

    async def test_not_super_get_users(self, client, create_user):
        user = await create_user()
        jwt_header = get_jwt_header(user)

        resp = await client.get(settings.API_PATH + "/users", headers=jwt_header)

        assert resp.status_code == 403, resp.text
        assert resp.json() == {"detail": "Forbidden"}
