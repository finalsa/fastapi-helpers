from os import path
from json import loads
from fastapi_helpers.crud import BaseCrud


class DbSeeder():

    crud = None

    def __init__(self, crud_module) -> None:
        self.crud = crud_module

    async def read_index(
        self, 
        main_path:str="../seeds/", 
        index_path:str="index.json"
    ) -> bool:
        index = open(path.join(main_path, index_path), "r")
        index_content = "".join(index.readlines())
        index.close()
        classes = loads(index_content)
        for cls in classes:
            fil = open(path.join(main_path, f"{cls['name']}.json"), "r")
            fil_content = "".join(fil.readlines())
            fil.close()
            objects = loads(fil_content)
            crud_obj: BaseCrud = eval(f"self.crud.{cls['crud']}")
            for obj in objects:
                await crud_obj.create(obj)
        return True
