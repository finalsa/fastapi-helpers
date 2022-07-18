from typing import Dict, Any
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, status, Request
from logging import getLogger
from time import time
from json import dumps


class HeadersMiddleware(BaseHTTPMiddleware):
    headers: Dict = {}

    def __init__(self, app, headers: Dict = None):
        super().__init__(app)
        if headers is not None:
            self.headers = headers
        self.logger = getLogger("fastapi")

    async def dispatch(self, request: Request, call_next) -> Any:
        start_time = time()
        try:
            response = await call_next(request)
        except Exception as ex:
            self.logger.error("Exception: %s", ex)
            self.logger.exception(ex, exc_info=True)
            response = Response(
                dumps({"status": "An error has occurred"}),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {}
            )
        for header in self.headers:
            response.headers[header] = self.headers[header]
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
