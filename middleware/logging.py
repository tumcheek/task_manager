import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")

        logger.info(f"{method} {path} from {client_ip} using {user_agent}")

        response = await call_next(request)

        return response
