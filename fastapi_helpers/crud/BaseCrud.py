from ormar import Model
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult
from fastapi_helpers.routes.Paginate import paginate_object, load_data_callback
from typing import (
    List, Type, Optional, Dict, TypeVar, Union,
    Generic
)
from functools import lru_cache
from uuid import uuid4

T = TypeVar('T', bound=Model)


class BaseCrud(Generic[T]):
    search_attrs = []

    def __init__(
            self,
            model: Type[T]
    ) -> None:
        self.pk_type: Type = model.pk._field.__type__
        self.model = model

    @lru_cache(maxsize=32)
    def should_generate_id(self, ):
        if self.pk_type is str:
            return True
        return False

    async def get_list(
            self,
            options: PaginateOptions
    ) -> Union[List[T], PaginateResult[T]]:
        if options.filters == '':
            r = await paginate_object(
                self.model,
                options,
                (load_data, {})
            )
            return r
        else:
            return await self.search(options)

    async def search(
            self,
            options: PaginateOptions
    ) -> Union[List[T], PaginateResult[T]]:
        searchable = {}
        for item in self.search_attrs:
            searchable[item + "__icontains"] = options.filters
        options.or_filters = searchable
        return await paginate_object(
            self.model,
            options,
            (load_data, {})
        )

    async def get(
            self,
            model_id: Union[int, str]
    ) -> Optional[Union[T, Dict]]:
        options = PaginateOptions()
        options.limit = 1
        options.filters = {'id': model_id}
        objs = await paginate_object(
            self.model,
            options,
            (load_data, {})
        )
        if len(objs) > 0:
            return objs[0]
        return None

    async def get_or_create(
            self,
            model_in: Union[T, Dict]
    ) -> Union[T, Dict]:
        params = to_dict(model_in)
        obj = await self.model.objects.get_or_none(**params)
        if obj is None:
            return await self.create(model_in)
        return obj

    async def create(
            self,
            model_in: Union[T, Dict]
    ) -> Optional[Union[T, Dict]]:
        params = to_dict(model_in)
        obj = self.model(**params)
        if self.should_generate_id():
            obj.id = str(uuid4())
        obj = await obj.save()
        return obj

    async def update(
            self,
            model_id: Optional[Union[int, str]],
            model_in: Union[T, Dict]
    ) -> Optional[Union[T, Dict]]:
        params = to_dict(model_in)
        obj = await self.model.objects.get_or_none(id=model_id)
        if obj is None:
            return None
        obj = await obj.update(**params)
        return obj

    async def delete(
            self,
            model_id: Optional[Union[int, str]]
    ) -> Optional[Union[T, Dict]]:
        obj = await self.model.objects.get_or_none(id=model_id)
        if obj is None:
            return None
        await obj.delete()
        return obj


def to_dict(
        model_in:
        Union[T, Dict]
) -> Dict:
    if isinstance(model_in, dict):
        params = model_in
    else:
        params = model_in.dict(exclude_unset=True)
    for key in params:
        item = params[key]
        if isinstance(item, dict) and 'id' in item:
            params[key] = item['id']
    return params


async def load_data(
        result=None
) -> List[T]:
    if result is None:
        result = []
    return await load_data_callback(result)
