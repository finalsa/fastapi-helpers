from ormar import Model
from fastapi_helpers.routes.Paginate import paginate_object, load_data_callback, Pagination
from typing import Any, List, Type, Optional, Dict, Union


class BaseCrud():

    search_attrs = []

    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    async def load_data(self, result:List[Model] =[]) -> List[Model]:
        return await load_data_callback(result)

    async def get_list(self, options: Pagination) -> List[Any]:
        if(options.search == ''):
            r = await paginate_object(
                self.model,
                options,
                (self.load_data, {})
            )
            return r
        else:
            return await self.search(options)

    async def search(self, options: Pagination):
        searchable = {}
        for item in self.search_attrs:
            searchable[item + "__icontains"] = options.search
        options.orable = searchable
        return await paginate_object(
            self.model,
            options,
            (self.load_data, {})
        )

    async def get(self, id: Optional[Union[int, str]]) -> Any:
        options = Pagination()
        options.limit = 1
        options.filters = {'id': id}
        objs = await paginate_object(
            self.model,
            options,
            (self.load_data, {})
        )
        if(len(objs) > 0):
            return objs[0]
        return None

    async def get_or_create(self, model_in: Optional[Union[Dict, Model]]) -> Optional[Model]:
        params = to_dict(model_in)
        obj = await self.model.objects.get_or_create(**params)
        return obj

    async def create(self, model_in: Optional[Union[Dict, Model]]) -> Optional[Model]:
        params = to_dict(model_in)
        obj = self.model(**params)
        obj = await obj.save()
        return obj

    async def update(
        self,
        id: Optional[Union[int, str]],
        model_in: Optional[Union[Dict, Model]]
    ) -> Optional[Model]:
        params = to_dict(model_in)
        obj = await self.model.objects.get_or_none(id=id)
        if(obj is None):
            return None
        obj = await obj.update(**params)
        return obj

    async def delete(self, id: Optional[Union[int, str]]) -> Optional[Model]:
        obj = await self.model.objects.get_or_none(id=id)
        if(obj is None):
            return None
        await obj.delete()
        return {'state': 'ok'}


def to_dict(model_in):
    params = {}
    if isinstance(model_in, dict):
        params = model_in
    else:
        params = model_in.dict(exclude_unset=True)
    for key in params:
        item = params[key]
        if isinstance(item, dict) and 'id' in item:
            params[key] = item['id']
    return params
