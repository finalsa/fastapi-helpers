from sqlalchemy.pool import NullPool
from db import DbConfig
import logging


class Worker:

    db_config: DbConfig

    @classmethod
    def use_db_connection(cls, func):
        '''Decorator that reports the execution time.'''

        async def wrap(*args, **kwargs):
            await cls.db_config.connect_db(NullPool)
            result = None
            try:
                result = await func(*args, **kwargs)
            except Exception as ex:
                logging.error(ex)
            await cls.db_config.disconnect_db()
            return result
        return wrap
