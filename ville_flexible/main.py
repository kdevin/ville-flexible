import logging

from fastapi import FastAPI

from ville_flexible.api import api_router
from ville_flexible import TITLE, VERSION

logger = logging.getLogger(__name__)

# we configure the logging level
logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title=TITLE,
    version=VERSION,
    openapi_url="/openapi.json",
)

# we add all API routes to the Web API framework
app.include_router(api_router)
