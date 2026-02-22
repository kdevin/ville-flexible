import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ville_flexible.api import api_router
from ville_flexible import TITLE, VERSION

logger = logging.getLogger(__name__)


app = FastAPI(
    title=TITLE,
    version=VERSION,
    openapi_url="/openapi.json",
)

# we add all API routes to the Web API framework
app.include_router(api_router)

# Exception handlers

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
