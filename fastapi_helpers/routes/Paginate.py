import ormar as orm
import math
from typing import Any, List, Optional, Dict, Tuple, Union


async def load_data_callback(
    result: List[orm.Model] = []
)-> List[orm.Model]:
    for r in result:
        await r.load_data()
    return result


class Pagination:

    def __init__(
        self,
        paginate: Optional[bool] = False,
        search: Optional[str] = '',
        objects_per_page: Optional[int] = 5,
        page: Optional[int] = 0,
        limit: Optional[int] = 5,
        order_by: Optional[str] = '-id',
    ):
        self.paginate = paginate
        self.objects_per_page = objects_per_page
        self.page = page
        self.limit = limit
        self.order_by = order_by.split(",")
        self.search = search
        self.filters = {}
        self.orable = {}

    def set_filters(self, **filters) -> None:
        if("pagination" in filters):
            filters.pop("pagination")
        if("objects_per_page" in filters):
            filters.pop("objects_per_page")
        if("page" in filters):
            filters.pop("page")
        if("limit" in filters):
            filters.pop("limit")
        if("order_by" in filters):
            filters.pop("order_by")
        if("search" in filters):
            filters.pop("search")
        self.filters = filters

    def __str__(self) -> str:
        return "pagination:{}, objects_per_page:{}, page:{}, limit:{}, order_by:{}, filters:{}".format(
            self.paginate,
            self.objects_per_page,
            self.page,
            self.limit,
            self.order_by,
            self.filters
        )


class PaginationResult():
    items_per_page: int
    total_objects: int
    total_pages: int
    actual_page: int
    data: List[Any]


async def paginate_object(
    model: orm.Model,
    options: Pagination = Pagination(),
    callback: Tuple = None
) -> Optional[Union[Dict, List]]:

    if hasattr(model, 'objects'):
        model = model.objects
    result = []
    query = model.filter(
        **options.filters
    )
    if(len(options.orable) > 0):
        query = query.filter(
            orm.or_(**options.orable)
        )
    if(options.limit == 0):
        offset = options.objects_per_page * options.page
        result = await query.offset(
            offset
        ).limit(
            options.objects_per_page
        ).order_by(
            options.order_by
        ).all()
    else:
        offset = options.objects_per_page * options.page
        result = await query.offset(
            offset
        ).limit(
            options.limit
        ).order_by(
            options.order_by
        ).all()
    if(callback is not None and len(callback) > 1):
        callback[1]['result'] = result
        result = await callback[0](** callback[1])
    if(options.paginate):
        total_objects = await query.count()
        total_pages = math.floor(total_objects / options.objects_per_page)
        if(total_objects % options.objects_per_page) > 0:
            total_pages += 1
        r = {
            'items_per_page':  options.objects_per_page,
            'total_objects': total_objects,
            'total_pages': total_pages,
            'actual_page': options.page,
            'data': result
        }
        return r
    else:
        return result
