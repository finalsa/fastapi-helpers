from typing import Dict, Optional, Union
from fastapi import (
    APIRouter, Request, Depends, 
    HTTPException, Response, status
)
from ormar import Model
from fastapi_helpers.crud import BaseCrud
from .Paginate import Pagination
from orjson import dumps



class DefaultModelRouter():

    router: APIRouter
    crud: BaseCrud
    model: Model
    headers: Dict
    NOT_FOUND_ERR = {
        "status": "not found"
    }

    def __init__(
        self,
        model: Model,
        crud: BaseCrud,
        headers: Dict = None
    ) -> None:
        self.model = model
        self.crud = crud
        id_label = "/{id}/"
        self.router = APIRouter()
        self.router.add_api_route("/", self.read_list, methods=["GET"])
        self.router.add_api_route(id_label, self.read, methods=["GET"])
        self.router.add_api_route("/", self.create, methods=["POST"])
        self.router.add_api_route(id_label, self.update, methods=["PUT"])
        self.router.add_api_route(id_label, self.delete, methods=["DELETE"])
        self.headers = headers

    async def read_list(
        self,
        *,
        request: Request,
        options: Pagination = Depends(),
    ):
        options.set_filters(**request.query_params._dict)
        r = await self.crud.get_list(options)
        return r

    async def read(
        self,
        *,
        id: int,
    ) -> Optional[Union[Model, Dict]]:
        m = await self.crud.get(id=id)
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        if(isinstance(m, Model)):
            return Response(dumps(m.dict()), status.HTTP_200_OK, self.headers)
        return Response(dumps(m), status.HTTP_200_OK, self.headers)

    async def create(
        self,
        *,
        model_in: Dict,
    ) -> Optional[Model]:
        m = await self.crud.create(
            model_in
        )
        if(isinstance(m, Model)):
            return Response(dumps(m.dict()), status.HTTP_201_CREATED, self.headers)
        return Response(dumps(m), status.HTTP_201_CREATED, self.headers,)

    async def update(
        self,
        *,
        id: int,
        model_in:  Dict,
    ) -> Optional[Model]:
        m = await self.crud.update(
            id,
            model_in
        )
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        if(isinstance(m, Model)):
            return Response(dumps(m.dict()), status.HTTP_202_ACCEPTED, self.headers)
        return Response(
            dumps(m), status.HTTP_202_ACCEPTED, self.headers
        )

    async def delete(
        self,
        *,
        id: int,
    ) -> Response:
        m = await self.crud.delete(
            id=id,
        )
        if(m is None):
            raise HTTPException(404, self.NOT_FOUND_ERR, self.headers)
        if(isinstance(m, Model)):
            return Response(dumps(m.dict()), status.HTTP_202_ACCEPTED, self.headers)
        return Response(
            dumps(m), status.HTTP_202_ACCEPTED, self.headers
        )
