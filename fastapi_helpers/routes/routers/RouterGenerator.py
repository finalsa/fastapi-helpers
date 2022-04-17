from fastapi import APIRouter
from ormar import Model
from typing import Type, Dict, NewType
from fastapi_helpers.crud import BaseCrud
from typing import (
    List, Dict, Optional, Union, TypeVar
)
from fastapi import (
    APIRouter, Request, Depends,
)
from fastapi_helpers.crud import BaseCrud
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult
from fastapi_helpers.routes.routers.DefaultModelRouter import DefaultModelRouter


ID_ROUTE_LABEL = "/{id}/"

T = TypeVar("T", bound = Model)

def get_router(
    model: Type[Model],
    crud: BaseCrud[T],
    headers: Dict = None,
    model_in: Optional[Type[T]] = None,
    model_out: Optional[Type[T]] = None,
) -> DefaultModelRouter[T]:

    model_name = model.get_name()
    ModelType = NewType(f"{model_name}", model)
    key_type = model.pk._field.__type__

    if model_in is None:
        ModelIn = NewType(f"{model_name}In", model.get_pydantic())
    else:
        ModelIn = model_in

    if model_out is None:
        ModelOut = NewType(f"{model_name}Out", model.get_pydantic())
    else:
        ModelOut = model_out
    
    KeyType = NewType(f"{model_name}_{key_type}", key_type)

    class ModelRouter(DefaultModelRouter):

        def __init__(
            self,
            model: ModelType,
            crud: BaseCrud,
            headers: Dict = None,
            response_model: Optional[ModelOut] = None,
        ) -> None:
            self.model = model
            self.crud = crud
            self.router = APIRouter()
            self.response_model = response_model
            self.router.add_api_route("/", self.read_list, methods=["GET"])
            self.router.add_api_route(ID_ROUTE_LABEL, self.read, methods=["GET"])
            self.router.add_api_route("/", self.create, methods=["POST"])
            self.router.add_api_route(ID_ROUTE_LABEL, self.update, methods=["PUT"])
            self.router.add_api_route(ID_ROUTE_LABEL, self.delete, methods=["DELETE"])
            self.headers = headers

        async def read_list(
            self,
            *,
            request: Request,
            options: PaginateOptions = Depends(),
        ) -> Union[Union[List[ModelOut], PaginateResult[ModelOut]], Dict]:
            return await super().read_list(
                request=request,
                options=options,
            )

        async def read(
            self,
            *,
            id: KeyType,
        ) -> Optional[Union[ModelOut, Dict]]:
            return await super().read(
                id=id,
            )

        async def create(
            self,
            *,
            model_in: ModelIn,
        ) -> Optional[Union[ModelOut, Dict]]:
            return await super().create(
                model_in=model_in,
            )

        async def update(
            self,
            *,
            id: KeyType,
            model_in: Union[ModelIn, Dict],
        ) -> Optional[Union[ModelOut, Dict]]:
            return await super().update(
                id=id,
                model_in=model_in,
            )

        async def delete(
            self,
            *,
            id: KeyType,
        ) -> Optional[Union[ModelOut, Dict]]:
            return await super().delete(
                id=id,
            )

    if model_out:
        return ModelRouter(model, crud, headers, ModelOut)
    return ModelRouter(model, crud, headers,)