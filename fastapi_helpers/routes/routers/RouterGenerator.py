from typing import (
    List, Dict, Optional, Union, TypeVar,
    Callable
)
from typing import Type, NewType

from fastapi import (
    Request, Depends,
)
from ormar import Model
from pydantic import BaseModel

from fastapi_helpers.crud import BaseCrud
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult
from fastapi_helpers.routes.routers.DefaultModelRouter import DefaultModelRouter

ID_ROUTE_LABEL = "/{id}/"

T = TypeVar("T", bound=Model)

pydantic_instances: Dict[str, Type[BaseModel]] = {}


def get_router(
        base_model: Union[T, Type[Model]],
        base_crud: BaseCrud[T],
        output_headers: Dict = None,
        model_in_type: Optional[Union[Type[BaseModel], Type[Model]]] = None,
        model_out_type: Optional[Union[Type[BaseModel], Type[Model]]] = None,

) -> DefaultModelRouter[T]:
    global pydantic_instances
    model_name = base_model.get_name()

    if model_name not in pydantic_instances:
        pydantic_instances[model_name] = base_model.get_pydantic()

    pydantic_instance = pydantic_instances[model_name]

    model_type = pydantic_instance
    key_type = base_model.pk._field.__type__

    if model_in_type is None:
        model_in_type = pydantic_instance
    else:
        model_in_type = model_in_type

    if model_out_type is None:
        model_out_type = pydantic_instance
    else:
        model_out_type = model_out_type

    key_type = NewType(f"{model_name}_{key_type}", key_type)

    class ModelRouter(DefaultModelRouter):

        def __init__(self, model: Union[T, Type[BaseModel]], crud: BaseCrud[T], headers: Optional[Dict] = None,
                     response_model: Optional[Callable[[Dict], BaseModel]] = None) -> None:
            super().__init__(model, crud, headers, response_model)

        async def read_list(
                self,
                *,
                request: Request,
                options: PaginateOptions = Depends(),
        ) -> Union[Union[List[model_out_type], PaginateResult[model_out_type]], Dict]:
            return await super().read_list(
                request=request,
                options=options,
            )

        async def read(
                self,
                *,
                model_id: key_type,
        ) -> Optional[Union[model_out_type, Dict]]:
            return await super().read(
                model_id=model_id,
            )

        async def create(
                self,
                *,
                model_in: Union[model_in_type, Dict],
        ) -> Optional[Union[model_out_type, Dict]]:
            return await super().create(
                model_in=model_in,
            )

        async def update(
                self,
                *,
                model_id: key_type,
                model_in: Union[model_in_type, Dict],
        ) -> Optional[Union[model_out_type, Dict]]:
            return await super().update(
                model_id=model_id,
                model_in=model_in,
            )

        async def delete(
                self,
                *,
                model_id: key_type,
        ) -> Optional[Union[model_out_type, Dict]]:
            return await super().delete(
                model_id=model_id,
            )

    if model_out_type:
        return ModelRouter(base_model, base_crud, output_headers, model_out_type)
    return ModelRouter(model_type, base_crud, output_headers, )
