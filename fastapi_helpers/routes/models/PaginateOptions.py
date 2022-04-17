from typing import Optional, Generic

class PaginateOptions():

    def __init__(
        self,
        paginate: Optional[bool] = False,
        filters: Optional[str] = '',
        objects_per_page: Optional[int] = 5,
        page: Optional[int] = 0,
        limit: Optional[int] = 0,
        order_by: Optional[str] = '-id',
    ):
        self.paginate = paginate
        self.objects_per_page = objects_per_page
        self.page = page
        self.limit = limit
        self.order_by = order_by.split(",")
        self.filters = filters
        self.filters = {}
        self.orable = {}

    def set_filters(self, **filters) -> None:
        if("pagination" in filters):
            filters.pop("pagination")
        if("paginate" in filters):
            filters.pop("paginate")
        if("objects_per_page" in filters):
            filters.pop("objects_per_page")
        if("page" in filters):
            filters.pop("page")
        if("limit" in filters):
            filters.pop("limit")
        if("order_by" in filters):
            filters.pop("order_by")
        if("filters" in filters):
            filters.pop("filters")
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
