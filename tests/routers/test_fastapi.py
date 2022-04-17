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
        pass

    id: int = ormar.Integer(primary_key=True)
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


crud = BaseCrud(Item)

router = get_router(Item, crud, model_in=ItemRequest, model_out=ItemResult)


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


app.include_router(router.router, )
worker = Worker(db_config)


client = TestClient(app)


@pytest.mark.asyncio()
async def test_read_main():
    await crud.create(Item(name="test", id=1))
    response = client.request("GET", "/")
    assert len(response.json()) == 1
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_read_one():
    response = client.request("GET", "/1/")
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "test"
    assert item["pydantic_int"] is None
    assert "password" not in item
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_read_none():
    response = client.request("GET", "/100/")
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_write_one():
    response = client.request("POST", "/", json={"name": "test2", "password" : "test"})
    assert response.status_code == 201


@pytest.mark.asyncio()
async def test_update_one():
    response = client.request("PUT", "/1/", json={"name": "test3"})
    assert response.status_code == 202


@pytest.mark.asyncio()
async def test_update_none():
    response = client.request("PUT", "/100/", json={"name": "test3"})
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_delete_one():
    response = client.request("DELETE", "/1/")
    assert response.status_code == 202


@pytest.mark.asyncio()
async def test_delete_none():
    response = client.request("DELETE", "/1000/")
    assert response.status_code == 404
