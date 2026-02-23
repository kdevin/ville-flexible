from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from ville_flexible.activation.service import (
    ActivationService,
    CheapestAssetCoveringRequestVolumeStrategy,
)
from ville_flexible.asset.models import Asset
from ville_flexible.asset.service import AssetService
from ville_flexible.config import Settings
from ville_flexible.data.database import get_assets


@lru_cache
def get_assets_from_db():
    return [Asset(**asset_data) for asset_data in get_assets()]


AssetsDep = Annotated[Settings, Depends(get_assets_from_db)]


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_asset_service(assets: AssetsDep):
    return AssetService(assets)


AssetServiceDep = Annotated[AssetService, Depends(get_asset_service)]


def get_activation_service(settings: SettingsDep, asset_service: AssetServiceDep):
    match settings.strategy:
        case "cheapest_asset_covering_request_volume":
            selected_strategy = CheapestAssetCoveringRequestVolumeStrategy()
        case _:
            raise ValueError(f"Unknown strategy: {settings.strategy}")

    return ActivationService(asset_service=asset_service, strategy=selected_strategy)


ActivationServiceDep = Annotated[ActivationService, Depends(get_activation_service)]
