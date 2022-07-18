from os import path
from json import loads
from fastapi_helpers.crud import BaseCrud
from logging import getLogger


class DbSeeder:
    crud = None

    def __init__(self, crud_module) -> None:
        self.crud = crud_module

    async def read_index(
            self,
            main_path: str = "../seeds/",
            index_path: str = "index.json"
    ) -> bool:
        logger = getLogger("fastapi")
        logger.info("Reading index file", extra={"path": index_path, "main_path": main_path, "crud": self.crud})
        index = open(path.join(main_path, index_path), "r")
        index_content = "".join(index.readlines())
        index.close()
        classes = loads(index_content)
        for cls in classes:
            fil = open(path.join(main_path, f"{cls['name']}.json"), "r")
            logger.info(f"Reading {cls['name']}")
            fil_content = "".join(fil.readlines())
            fil.close()
            objects = loads(fil_content)
            crud_obj: BaseCrud = eval(f"self.crud.{cls['crud']}")
            logger.info(f"Seeding {cls['name']}")
            for obj in objects:
                logger.info(f"Seeding {cls['name']} {obj['id']}")
                await crud_obj.create(obj)
            logger.info(f"Seeded {cls['name']}")
        return True
