from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ville_flexible.asset.views import router as asset_router
from ville_flexible.activation.views import router as activation_router


class ErrorMessage(BaseModel):
    """Represents a single error message."""

    msg: str


class ErrorResponse(BaseModel):
    """Defines the structure for API error responses."""

    detail: list[ErrorMessage] | None = None


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

api_router.include_router(asset_router)
api_router.include_router(activation_router)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    """Simple healthcheck endpoint."""
    return {"status": "ok"}


@api_router.get("/helloworld")
def helloworld():
    """Returns a simple "Hello World!" message."""
    return "Hello World!"
