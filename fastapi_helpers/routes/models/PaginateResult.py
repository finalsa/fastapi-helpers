import ormar as orm
from pydantic import BaseModel
from typing import (
    Dict, List, Any, TypeVar,
    Generic
)

T = TypeVar('T', orm.Model, BaseModel, Dict)

class PaginateResult(BaseModel, Generic[T]):

    items_per_page: int
    total_objects: int
    total_pages: int
    actual_page: int
    data: List[T]

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
    
    def __str__(self) -> str:
        return "items_per_page:{}, total_objects:{}, total_pages:{}, actual_page:{}, data:{}".format(
            self.items_per_page,
            self.total_objects,
            self.total_pages,
            self.actual_page,
            self.data
        )