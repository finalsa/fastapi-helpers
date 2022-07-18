from typing import (
    List, Dict, Optional, Union,
    TypeVar, Generic, Callable
)

from fastapi import (
    APIRouter, Request, Depends,
    HTTPException, Response, status
)
from ormar import Model
from pydantic import BaseModel

from fastapi_helpers.crud import BaseCrud
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult

try:
    from orjson import dumps
except ImportError:
    from json import dumps


class ErrorSchema(BaseModel):
    status: str
    content: str
    traceback: str


ID_ROUTE_LABEL = "/{model_id}/"

T = TypeVar("T", bound=Model)


class DefaultModelRouter(Generic[T]):
    router: APIRouter
    crud: BaseCrud[T]
    model: T
    headers: Dict
    NOT_FOUND_ERR = {
        "status": "not found"
    }

    def __init__(
            self,
            model: T,
            crud: BaseCrud[T],
            headers: Optional[Dict] = None,
            response_model: Optional[Callable[[Dict], BaseModel]] = None,
    ) -> None:
        self.model = model
        self.crud = crud
        self.response_model = response_model
        self.router = APIRouter()
        self.model = model
        self.crud = crud
        self.router = APIRouter()
        self.response_model = response_model
        class_name = self.model.__name__
        if response_model is not None:
            helper_response_model = response_model
        else:
            helper_response_model = model.get_pydantic()

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
    ) -> Union[Response, List]:
        params = dict(request.query_params)
        options.set_filters(**params)
        r = await self.crud.get_list(options)
        if isinstance(r, PaginateResult):
            r.data = self.parse_response(r.data)
            return Response(
                dumps(r.dict()), status.HTTP_200_OK, self.headers
            )
        return self.parse_response(r)

    async def read(
            self,
            *,
            model_id,
    ) -> Union[Response, Optional[Union[T, Dict]]]:
        m = await self.crud.get(model_id=model_id)
        return self.get_response(m, status.HTTP_200_OK)

    async def create(
            self,
            *,
            model_in: Union[T, Dict],
    ) -> Union[Response, Optional[Union[T, Dict]]]:
        """
        Create a new model.
        """
        m = await self.crud.create(
            model_in
        )
        return self.get_response(m, status.HTTP_201_CREATED)

    async def update(
            self,
            *,
            model_id,
            model_in: Union[T, Dict],
    ) -> Union[Response, Optional[Union[T, Dict]]]:
        m = await self.crud.update(
            model_id,
            model_in
        )
        return self.get_response(m, status.HTTP_202_ACCEPTED)

    async def delete(
            self,
            *,
            model_id,
    ) -> Union[Response, Optional[Union[T, Dict]]]:
        m = await self.crud.delete(
            model_id=model_id,
        )
        return self.get_response(m, status.HTTP_202_ACCEPTED)

    def get_response(self, m: Optional[Union[Model, BaseModel]], ok_status: int) -> Response:
        if m is None:
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        m = self.parse_response([m])[0]
        if isinstance(m, Model) or isinstance(m, BaseModel):
            return Response(
                dumps(m.dict()),
                ok_status,
                self.headers,
                media_type="application/json"
            )
        return Response(
            dumps(m),
            ok_status,
            self.headers,
            media_type="application/json"
        )

    def parse_response(
            self,
            items: List[Union[Dict, T]],
    ) -> List:
        if self.response_model is None:
            return items
        if len(items) > 0:
            if isinstance(items[0], dict):
                return [self.response_model(**item) for item in items]
            return [self.response_model(**item.dict()) for item in items]
        return items
