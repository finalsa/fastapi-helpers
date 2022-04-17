
from typing import Any, List
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, status, Request
from .get_real_ip import get_real_ip
from logging import getLogger
from orjson import dumps


class IpAccessMiddleware(BaseHTTPMiddleware):

    accepted_ips: List[str]

    def __init__(
        self,
        app,
        accepted_ips: List[str] = []
    ):
        super().__init__(app)
        self.logger = getLogger("fastapi")
        self.accepted_ips = accepted_ips

    async def dispatch(self, request: Request, call_next) -> Any:
        response = None
        ip = get_real_ip(request)
        if(ip not in self.accepted_ips):
            response = Response(
                dumps({"status": "Access denied"}),
                status.HTTP_403_FORBIDDEN,
                media_type="application/json"
            )
        else:
            response = await call_next(request)
        return response
