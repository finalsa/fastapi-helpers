import sys
import os
import logging
import logging.config
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi_helpers import (DefaultSettings, get_logger_default_config)

settings = DefaultSettings()
settings.env = "test"

app = FastAPI()

logging.config.dictConfig(get_logger_default_config(settings))
logger = logging.getLogger("fastapi")


@app.get("/")
async def root():
    logger.info("Houston, we have a problem: %s", "test info", exc_info=1, extra={"id": 10000123})
    logger.error("Houston, we have a problem: %s", "error info", exc_info=1, extra={"error": "tes"})
    logger.critical({"request": "hello", "metadata": {"size": 9000}})
    try:
        raise Exception("test")
    except Exception as ex:
        logger.exception(ex)

    v = app.title
    return {"message": v}


client = TestClient(app)


def test_logging():
    for _ in range(1, 100):
        r = client.get("/")
        assert r.status_code == 200
