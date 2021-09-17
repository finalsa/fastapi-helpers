from sqlalchemy.pool import NullPool
from fastapi_helpers.db import DbConfig
from fastapi_helpers.logging import DefaultLogger

class Worker:

    db_config: DbConfig
    logger: DefaultLogger

    def __init__(self, db_config:DbConfig, logger: DefaultLogger) -> None:
        self.db_config = db_config
        self.logger  = logger

    def use_db_connection(self, func):
        '''Decorator that reports the execution time.'''

        async def wrap(*args, **kwargs):
            await self.db_config.connect_db(NullPool)
            result = None
            try:
                result = await func(*args, **kwargs)
            except Exception as ex:
                self.logger.error(ex)
            await self.db_config.disconnect_db()
            return result
        return wrap
