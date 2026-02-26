from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ville_flexible.asset.models import Asset, WeekDay
from ville_flexible.dependencies import AssetServiceDep

router = APIRouter(tags=["assets"], prefix="/assets")


@router.get("/", response_model=list[Asset])
def list(asset_service: AssetServiceDep, week_day: WeekDay | None = None):
    return asset_service.list(week_day=week_day)


@router.get("/{asset_code}", response_model=Asset)
def retrieve(asset_service: AssetServiceDep, asset_code: str):
    try:
        return asset_service.retrieve(asset_code)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


@router.post("/", response_model=Asset)
def create(asset_service: AssetServiceDep, asset: Asset):
    try:
        return asset_service.create(asset)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


@router.delete("/{asset_code}")
def delete(asset_service: AssetServiceDep, asset_code: str):
    try:
        asset_service.delete(asset_code)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
