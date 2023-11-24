# Exception middleware
import sys
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from logger_info import logger


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            logger.debug("Our custom unhandled_exception_handler was called")

            # ? Check Authorization Header and get token
            authorization_header = request.headers.get("Authorization")

            # ? Split the authorization header to get the scheme and token
            scheme, token = (
                authorization_header.split()
                if authorization_header
                else (
                    None,
                    None,
                )
            )
            # ? Check if the token is valid or not here to get user info
            """
                Logic to get user info from token should be here
            """
            # ? Check Content-Type
            content_type = request.headers.get("Content-Type")
            host = getattr(getattr(request, "client", None), "host", None)
            port = getattr(getattr(request, "client", None), "port", None)
            url = (
                f"{request.url.path}?{request.query_params}"
                if request.query_params
                else request.url.path
            )

            # ? Get the request params
            get_params = (
                request.query_params if request.query_params else "No Request Params"
            )

            # ? Get the request body as a UTF-8 string
            body_bytes = await request.body()
            if body_bytes and "application/json" in content_type:
                body_text = body_bytes.decode("utf-8")
            else:
                body_text = body_bytes
            post_body = body_bytes if body_bytes else "No Request Body"

            # ? Exception details
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, "__name__", None)

            # ? Log the exception
            logger.error(
                f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value} >'
            )

            return JSONResponse(
                status_code=500, content={"detail": "Internal Server Error"}
            )
