from types import MethodWrapperType
from sqlalchemy.pool import NullPool
from fastapi_helpers.db import DbConfig
from logging import getLogger
from typing import Any

class Worker:

    db_config: DbConfig

    def __init__(
        self,
        db_config: DbConfig,
    ) -> None:
        self.db_config = db_config
        self.logger = getLogger("fastapi")

    def use_db_connection(self, func) -> MethodWrapperType:
        '''Decorator that connects to the db.'''
        async def wrap(*args, **kwargs) -> Any:
            await self.db_config.connect_db(NullPool)
            result = None
            try:
                result = await func(*args, **kwargs)
            except Exception as ex:
                self.logger.error(ex)
            await self.db_config.disconnect_db()
            return result
        return wrap
