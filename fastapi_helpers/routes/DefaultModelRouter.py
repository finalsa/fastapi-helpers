from typing import Any, Dict
from fastapi import APIRouter, Request, Depends
from ormar import Model
from fastapi_helpers.crud import BaseCrud
from .Paginate import Pagination


class DefaultModelRouter():

    router = None
    crud: BaseCrud
    model: Model

    def __init__(self, model: Model, crud: BaseCrud) -> None:
        self.model = model
        self.crud = crud
        self.router = APIRouter()
        self.router.add_api_route("/", self.read_list, methods=["GET"])
        self.router.add_api_route("/{id}/", self.read, methods=["GET"])
        self.router.add_api_route("/", self.create, methods=["POST"])
        self.router.add_api_route("/{id}/", self.update, methods=["PUT"])
        self.router.add_api_route("/{id}/", self.delete, methods=["DELETE"])


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
    ):
        return await self.crud.get(id=id)

    async def create(
        self,
        *,
        model_in: Dict,
    ) -> Any:

        return await self.crud.create(
            model_in
        )

    async def update(
        self,
        *,
        id: int,
        model_in:  Dict,
    ):
        return await self.crud.update(
            id,
            model_in
        )
    
    async def delete(
        self,
        *,
        id: int,
    ):
        return await self.crud.delete(
            id=id,
        )

    