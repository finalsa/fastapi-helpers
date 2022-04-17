from email.policy import default
import uuid
import ormar
from fastapi import FastAPI
import sqlalchemy
import pytest
import databases
from fastapi_helpers import (
    DbConfig,
    DefaultSettings,
    BaseCrud,
    Worker,
    get_logger_default_config,
)
from typing import Optional
import logging
import logging.config
from fastapi.testclient import TestClient
import sys
import os

import pydantic
from fastapi_helpers.routes.routers.RouterGenerator import get_router

import pytest_asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


settings = DefaultSettings()
settings.env = "test"
logging.config.dictConfig(get_logger_default_config(settings))
logger = logging.getLogger("fastapi")
db_config = DbConfig(settings)


app = FastAPI()
metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite:///test.db", force_rollback=True)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


class LocalMeta:
    metadata = metadata
    database = database


class Item(ormar.Model):
    class Meta(LocalMeta):
        table_name = "items"
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    password: str = ormar.String(max_length=100, default='')
    pydantic_int: Optional[int]

    async def load_data(self):
        return self


class User(ormar.Model):
    class Meta(LocalMeta):
        table_name = "users"
        pass

    id: str = ormar.String(max_length=36, default="", primary_key=True)
    name: str = ormar.String(max_length=100)
    password: str = ormar.String(max_length=100, default='')
    pydantic_int: Optional[int]

    async def load_data(self):
        return self


class ItemResult(pydantic.BaseModel):

    id: int
    name: str
    pydantic_int: Optional[int]


class ItemRequest(pydantic.BaseModel):
    name: str
    password:  str


item_crud = BaseCrud(Item)
user_crud = BaseCrud(User)

item_router = get_router(Item, item_crud, model_in=ItemRequest, model_out=ItemResult)
user_router = get_router(User, user_crud, model_in=ItemRequest)


@pytest_asyncio.fixture(autouse=True, scope="module")
def create_test_database():
    engine = sqlalchemy.create_engine("sqlite:///test.db")
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


app = FastAPI(
    title="Tests",
    version=settings.version,
    on_startup=[db_config.connect_db],
    on_shutdown=[db_config.disconnect_db],
    openapi_url=settings.get_open_api_path()
)


app.include_router(item_router.router,  prefix="/items")
app.include_router(user_router.router, prefix="/users")

worker = Worker(db_config)


client = TestClient(app)


@pytest.mark.asyncio()
async def test_read_main():
    await item_crud.create(Item(name="test", id=1))
    response = client.request("GET", "/items/")
    assert len(response.json()) == 1
    await item_crud.create(Item(name="test"))
    response = client.request("GET", "/items/")
    assert len(response.json()) == 2
    assert response.status_code == 200



@pytest.mark.asyncio()
async def test_uuid_crud():
    await user_crud.create({"name":"test"})
    response = client.request("GET", "/users/")
    assert len(response.json()) == 1
    assert response.status_code == 200

@pytest.mark.asyncio()
async def test_read_one():
    response = client.request("GET", "/items/1/")
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "test"
    assert item["pydantic_int"] is None
    assert "password" not in item
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_read_none():
    response = client.request("GET", "/items/100/")
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_read_pagination():
    response = client.request("GET", "/items/?paginate=true&objects_per_page=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["items_per_page"] == 1



@pytest.mark.asyncio()
async def test_uuid_pagination():
    response = client.request("GET", "/users/?paginate=true&objects_per_page=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["items_per_page"] == 1
    helper_id = uuid.UUID(data["data"][0]["id"])
    assert helper_id.version == 4
    assert helper_id.is_safe

@pytest.mark.asyncio()
async def test_write_one():
    response = client.request(
        "POST", "/items/", json={"name": "test2", "password": "test"})
    assert response.status_code == 201


@pytest.mark.asyncio()
async def test_update_one():
    response = client.request("PUT", "/items/1/", json={"name": "test3"})
    assert response.status_code == 202


@pytest.mark.asyncio()
async def test_update_none():
    response = client.request("PUT", "/items/100/", json={"name": "test3"})
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_delete_one():
    response = client.request("DELETE", "/items/1/")
    assert response.status_code == 202


@pytest.mark.asyncio()
async def test_delete_none():
    response = client.request("DELETE", "/items/1000/")
    assert response.status_code == 404
