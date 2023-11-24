from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# Custom exception handler for Pydantic validation errors
async def custom_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_details = []
    for error in exc.errors():
        loc = ".".join(error["loc"])
        msg = error["msg"]
        type_ = error["type"]
        error_details.append({"loc": loc, "msg": msg, "type": type_})
    response_data = {"detail": error_details[-1]}
    return JSONResponse(content=response_data, status_code=400)
