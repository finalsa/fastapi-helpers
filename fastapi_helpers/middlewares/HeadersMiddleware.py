from typing import Dict, Any
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, status, Request
from fastapi_helpers.logging import DefaultLogger
from time import time

class HeadersMiddleware(BaseHTTPMiddleware):

    headers: Dict = {}
    logger: DefaultLogger

    def __init__(self, app, headers: Dict = None, logger: DefaultLogger = None):
        super().__init__(app)
        if(headers is not None):
            self.headers = headers
        self.logger = logger

    async def dispatch(self, request:Request, call_next) -> Any:
        start_time = time()
        response = None
        try:
            response = await call_next(request)
        except Exception as ex:
            self.logger.error("Exception: %s", ex)
            self.logger.exception(ex)
            response = Response(
                {"status": "An error has ocurred"},
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                {}
            )
        for header in self.headers:
            response.headers[header] = self.headers[header]
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
