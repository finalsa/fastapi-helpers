from typing import (
    List, Dict, Optional, Union,
    TypeVar, Generic
)
from fastapi import (
    APIRouter, Request, Depends,
    HTTPException, Response, status
)
from pydantic import BaseModel
from ormar import Model
from fastapi_helpers.crud import BaseCrud
from fastapi_helpers.routes.models import PaginateOptions, PaginateResult
try:
    from orjson import dumps
except ImportError:
    from json import dumps
ID_ROUTE_LABEL = "/{id}/"

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
        response_model: Optional[BaseModel] = None,
    ) -> None:
        self.model = model
        self.crud = crud
        self.response_model = response_model
        self.router = APIRouter()
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
    ) -> Optional[Union[List[T], PaginateResult[T]]]:
        options.set_filters(**request.query_params._dict)
        r = await self.crud.get_list(options)
        return self.parse_response(r)

    def parse_response(
        self,
        items: List[Union[Dict, T]],
    ) -> List:
        if self.response_model is not None:
            if len(items) > 0:
                if isinstance(items[0], dict):
                    return [self.response_model(**item) for item in items]
                return [self.response_model(**item.dict()) for item in items]
        return items

    async def read(
        self,
        *,
        id,
    ) -> Optional[Union[T, Dict]]:
        m = await self.crud.get(id=id)
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        m = self.parse_response([m])[0]
        if(isinstance(m, Model) or isinstance(m, BaseModel)):
            return Response(dumps(m.dict()), status.HTTP_200_OK, self.headers)
        return Response(dumps(m), status.HTTP_200_OK, self.headers)

    async def create(
        self,
        *,
        model_in: Union[T, Dict],
    ) -> Optional[Union[T, Dict]]:
        m = await self.crud.create(
            model_in
        )
        m = self.parse_response([m])[0]
        if(isinstance(m, Model) or isinstance(m, BaseModel)):
            return Response(dumps(m.dict()), status.HTTP_201_CREATED, self.headers)
        return Response(dumps(m), status.HTTP_201_CREATED, self.headers,)

    async def update(
        self,
        *,
        id,
        model_in: Union[T, Dict],
    ) -> Optional[Union[T, Dict]]:
        m = await self.crud.update(
            id,
            model_in
        )
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        m = self.parse_response([m])[0]
        if(isinstance(m, Model) or isinstance(m, BaseModel)):
            return Response(dumps(m.dict()), status.HTTP_202_ACCEPTED, self.headers)
        return Response(
            dumps(m), status.HTTP_202_ACCEPTED, self.headers
        )

    async def delete(
        self,
        *,
        id,
    ) -> Optional[Union[T, Dict]]:
        m = await self.crud.delete(
            id=id,
        )
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        m = self.parse_response([m])[0]
        if(isinstance(m, Model) or isinstance(m, BaseModel)):
            return Response(dumps(m.dict()), status.HTTP_202_ACCEPTED, self.headers)
        return Response(
            dumps(m), status.HTTP_202_ACCEPTED, self.headers
        )
