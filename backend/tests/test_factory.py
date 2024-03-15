import pytest
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.responses import FileResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.factory import serve_static_app, use_route_names_as_operation_ids


class TestFactory:
    async def test_serve_static_app(self, client):
        # Test that the middleware is working for a non-existent route
        response = await client.get("/non_existent_route")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "Non-API route not found." in response.text

    async def test_existant_route(self, client):
        # Test that the middleware is not working for an existent route
        response = await client.get(settings.API_PATH + "/items")
        assert response.status_code == 401

    async def test_middleware_intercept_nonapi_route(self, client):
        # Test that the middleware is not working for an API route
        response = await client.get(settings.API_PATH + "/non_existent_route")
        assert response.status_code == 404

    async def test_no_middleware_intercept_docs_route(self, client):
        # Test that the middleware is not working for the docs route
        response = await client.get("/docs")
        assert response.status_code == 404

    async def test_use_route_names_as_operation_ids(self):
        app = FastAPI()

        @app.get("/route1", name="route1")
        async def route1():
            pass

        @app.get("/route2", name="route2")
        async def route2():
            pass

        use_route_names_as_operation_ids(app)

        for route in app.routes:
            if isinstance(route, APIRoute):
                assert route.operation_id == route.name

    async def test_use_route_names_as_operation_ites_dup(self, client):
        # Test that use_route_names_as_operation_ids raises an exception for duplicate route names
        app = FastAPI()

        @app.get("/route1", name="route1")
        async def route1():
            pass

        @app.get("/route2", name="route1")
        async def route2():
            pass

        with pytest.raises(Exception, match="Route function names should be unique"):
            use_route_names_as_operation_ids(app)
