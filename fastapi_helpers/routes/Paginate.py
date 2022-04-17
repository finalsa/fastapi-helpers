import ormar as orm
import pydantic as pd
import math
from typing import (
    List, Optional, Union,
    Callable, TypeVar, Dict,
    Tuple
)
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult

T = TypeVar('T', bound=orm.Model)


async def load_data_callback(
    items: List[T] = [],
) -> List[T]:
    if len(items) > 0:
        if hasattr(items[0], "load_data"):
            for r in items:
                await r.load_data()
    return items


async def get_paginate_result(
    result: List[T],
    query: orm.QuerySet,
    options: PaginateOptions = PaginateOptions(),
) -> PaginateResult[T]:
    total_objects = await query.count()
    total_pages = math.floor(total_objects / options.objects_per_page)
    if(total_objects % options.objects_per_page) > 0:
        total_pages += 1
    r = PaginateResult(
        items_per_page=options.objects_per_page,
        total_objects=total_objects,
        total_pages=total_pages,
        actual_page=options.page,
        data=result
    )
    return r


async def paginate_object(
    model: T,
    options: PaginateOptions = PaginateOptions(),
    load_data_action: Tuple[Callable[
        [List[T], Optional[pd.BaseModel]],
        List[T]
    ], Dict] = load_data_callback,
) -> Optional[
    Union[PaginateResult[T], List[T]]
]:
    if hasattr(model, 'objects'):
        model = model.objects
    result = []
    query: orm.QuerySet = model.filter(
        **options.filters
    )
    if(len(options.orable) > 0):
        query = query.filter(
            orm.or_(**options.orable)
        )
    offset = options.objects_per_page * options.page
    query = query.offset(
        offset
    )
    if(options.limit == 0):
        query.limit(
            options.objects_per_page
        )
    else:
        query.limit(
            options.limit
        )
    result = await query.order_by(
        options.order_by
    ).all()
    if load_data_action is not None and len(result)  == 2:
        result = await load_data_action[0](result, **load_data_action[1])
    if(options.paginate):
        return await get_paginate_result(result, query, options)
    else:
        return result
