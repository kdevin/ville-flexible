from typing import Annotated

from fastapi import Depends

from ville_flexible.activation.service import ActivationService
from ville_flexible.asset.models import Asset
from ville_flexible.asset.service import AssetService
from ville_flexible.data.database import get_assets


assets: list[Asset] = [Asset(**asset_data) for asset_data in get_assets()]


def get_asset_service():
    return AssetService(assets)


AssetServiceDep = Annotated[AssetService, Depends(get_asset_service)]


def get_activation_service(asset_service: AssetServiceDep):
    return ActivationService(asset_service=asset_service)


ActivationServiceDep = Annotated[ActivationService, Depends(get_activation_service)]