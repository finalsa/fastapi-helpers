from fastapi import APIRouter
from ormar import Model
from typing import Type, Dict, NewType
from pydantic import BaseModel
from fastapi_helpers.crud import BaseCrud
from typing import (
    List, Dict, Optional, Union, TypeVar
)
from fastapi import (
    APIRouter, Request, Depends,
)
from fastapi_helpers.crud import BaseCrud
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult
from fastapi_helpers.routes.routers.DefaultModelRouter import DefaultModelRouter, ErrorSchema


ID_ROUTE_LABEL = "/{id}/"

T = TypeVar("T", bound=Model)

pydantic_instances: Dict[str, Type[BaseModel]] = {}


def get_router(
    model: Type[Model],
    crud: BaseCrud[T],
    headers: Dict = None,
    model_in: Optional[Type[T]] = None,
    model_out: Optional[Type[T]] = None,

) -> DefaultModelRouter[T]:

    global pydantic_instances
    model_name = model.get_name()
    class_name = model.__name__

    if model_name not in pydantic_instances:
        pydantic_instances[model_name] = model.get_pydantic()

    pydantic_instance = pydantic_instances[model_name]

    ModelType = NewType(f"{model_name}", pydantic_instance)
    key_type = model.pk._field.__type__

    if model_in is None:
        ModelIn = NewType(f"{model_name}In", pydantic_instance)
    else:
        ModelIn = model_in

    if model_out is None:
        ModelOut = NewType(f"{model_name}Out", pydantic_instance)
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
            helper_response_model = None
            if response_model is not None:
                helper_response_model = response_model
            else:
                helper_response_model = pydantic_instance

            self.router.add_api_route(
                "/",
                self.read_list,
                methods=["GET"],
                summary=f"Read a list of {class_name}.",
                description=f"Read a list of {class_name}, you can use pagination or not.",
                responses={
                    200: {
                        "description": f"Read a list of {class_name}.",
                        "content": {
                            "application/json": {
                            },
                        }
                    },
                }
            )
            self.router.add_api_route(
                ID_ROUTE_LABEL,
                self.read,
                methods=["GET"],
                summary=f"Get a single instance of {class_name}.",
                description=f"Get a single instance of {class_name} by its id.",
                responses={
                    200: {
                        "description": f"Successfully retrieved {class_name}.",
                        "content": {
                            "application/json": {
                                "schema": helper_response_model.schema()
                            }
                        }
                    },
                    404: {
                        "description": f"Not found {class_name}.",
                        "content": {
                            "application/json": {
                                "schema": ErrorSchema.schema()
                            }
                        }
                    },
                }
            )
            self.router.add_api_route(
                "/",
                self.create,
                methods=["POST"],
                summary=f"Create a new instance of {class_name}.",
                description=f"Create a new instance of {class_name} .",
                status_code=201,
                responses={
                    201: {
                        "description": f"Successful creation of a {class_name} instance.",
                        "content": {
                            "application/json": {
                                "schema": helper_response_model.schema()
                            }
                        }
                    },
                }
            )
            self.router.add_api_route(
                ID_ROUTE_LABEL,
                self.update,
                methods=["PUT"],
                summary=f"Update an instance of {class_name}.",
                description=f"Update an instance of {class_name} by its id.",
                status_code=202,
                responses={
                    202: {
                        "description": f"Successfully updated {class_name}.",
                        "content": {
                            "application/json": {
                                "schema": helper_response_model.schema()
                            }
                        }
                    },
                    404: {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "schema": ErrorSchema.schema()
                                }
                            }
                        }
                    },
                }
            )
            self.router.add_api_route(
                ID_ROUTE_LABEL,
                self.delete,
                methods=["DELETE"],
                summary=f"Delete an instance of {class_name}.",
                description=f"Delete an instance of {class_name} by its id.",
                status_code=202,
                responses={
                    202: {
                        "description": f"Successfully deleted {class_name}.",
                        "content": {
                            "application/json": {
                                "schema": helper_response_model.schema()
                            }
                        }
                    },
                    404: {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "schema": ErrorSchema.schema()
                                }
                            }
                        }
                    },
                }
            )
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
