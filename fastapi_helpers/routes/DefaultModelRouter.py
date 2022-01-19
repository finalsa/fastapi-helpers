from typing import Dict, Optional, Union
from fastapi import (
    APIRouter, Request, Depends, 
    HTTPException, Response, status
)
from ormar import Model
from fastapi_helpers.crud import BaseCrud
from .Paginate import Pagination


class DefaultModelRouter():

    router: APIRouter
    crud: BaseCrud
    model: Model
    headers: Dict

    def __init__(
        self,
        model: Model,
        crud: BaseCrud,
        headers: Dict = None
    ) -> None:
        self.model = model
        self.crud = crud
        self.router = APIRouter()
        self.router.add_api_route("/", self.read_list, methods=["GET"])
        self.router.add_api_route("/{id}/", self.read, methods=["GET"])
        self.router.add_api_route("/", self.create, methods=["POST"])
        self.router.add_api_route("/{id}/", self.update, methods=["PUT"])
        self.router.add_api_route("/{id}/", self.delete, methods=["DELETE"])
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
            raise HTTPException(404, {
                "status": "not found"
            }, self.headers)
        return Response(m, status.HTTP_200_OK, self.headers, "")

    async def create(
        self,
        *,
        model_in: Dict,
    ) -> Optional[Model]:
        m = await self.crud.create(
            model_in
        )
        return Response(m, status.HTTP_201_CREATED, self.headers, )

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
            raise HTTPException(404, {
                "status": "not found"
            }, self.headers)
        return Response(
            m, status.HTTP_201_CREATED, self.headers
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
            return Response(
                {
                    "status": "not found"
                },
                status.HTTP_404_NOT_FOUND,
                self.headers
            )
        return Response(
            m, status.HTTP_202_ACCEPTED, self.headers
        )
