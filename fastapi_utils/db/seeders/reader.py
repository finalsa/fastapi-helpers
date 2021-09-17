from os import path
from json import loads
from fastapi_utils.crud import BaseCrud



async def read_index(main_path="../seeds/", index_path="index.json"):
    index = open(path.join(main_path, index_path), "r")
    index_content = "".join(index.readlines())
    index.close()
    classes = loads(index_content)
    for cls in classes:
        fil = open(path.join(main_path, cls['name'] + ".json"), "r")
        fil_content = "".join(fil.readlines())
        fil.close()
        objects = loads(fil_content)
        crud_obj: BaseCrud = eval("crud." + cls['crud'])
        for obj in objects:
            await crud_obj.create(obj)
    return True
