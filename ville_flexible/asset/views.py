from fastapi import APIRouter

from ville_flexible.asset.models import Asset, AvailableAsset
from ville_flexible.dependencies import AssetServiceDep

router = APIRouter(tags=["assets"], prefix="/assets")


@router.get("/", response_model=list[Asset])
def get_assets(asset_service: AssetServiceDep):
    return asset_service.assets


@router.get("/available", response_model=list[AvailableAsset])
def get_available_assets(week_day: int, asset_service: AssetServiceDep):
    return asset_service.get_available_assets(week_day)
