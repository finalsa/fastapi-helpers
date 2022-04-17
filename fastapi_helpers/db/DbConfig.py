from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool, Pool
from contextlib import closing
from fastapi_helpers.core.settings import DefaultSettings
from logging import getLogger


class DbConfig():

    engine: Engine
    db_url: str
    metadata: MetaData
    database: Database

    def __init__(
        self,
        settings: DefaultSettings,
    ) -> None:
        self.db_url = settings.get_db_url()
        self.metadata = MetaData()
        self.database = Database(self.db_url)
        self.logger = getLogger("fastapi")

    async def connect_db(
        self,
        poolclass: Pool = QueuePool
    ) -> None:
        if(self.database.is_connected):
            return
        self.engine = create_engine(
            self.db_url, poolclass=poolclass
        )
        self.metadata.create_all(self.engine)
        await self.database.connect()
        self.logger.info("DB connected")

    async def reset_db(self, ) -> None:
        with closing(self.engine.connect()) as con:
            trans = con.begin()
            for table in reversed(self.metadata.sorted_tables):
                con.execute(table.delete())
            trans.commit()
        self.logger.info("DB reseted")

    async def disconnect_db(self,) -> None:
        await self.database.disconnect()
        self.logger.info("DB disconnected")
