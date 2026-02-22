from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ville_flexible import TITLE, VERSION
from ville_flexible.api import api_router
from ville_flexible.config import Settings
from ville_flexible.logging import configure_logging

settings = Settings()

# Configure logging based on settings
# Define the logging configuration
configure_logging(settings.log_level)

# Create the FastAPI app instance
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
