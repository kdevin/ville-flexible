from typing import List

from ville_flexible.asset.models import Asset, AvailableAsset


class AssetService:
    def __init__(self, assets: List[Asset]):
        self.assets = assets

    def create(self, asset: Asset) -> Asset:
        if any(existing_asset.code == asset.code for existing_asset in self.assets):
            raise ValueError(f"Asset with code {asset.code} already exists")
        self.assets.append(asset)
        return asset

    def list(self, week_day: int | None = None) -> List[Asset]:
        if week_day is not None:
            return [asset for asset in self.assets if asset.is_available_on_date(week_day)]
        return self.assets

    def list_available(self, week_day: int) -> List[AvailableAsset]:
        return [AvailableAsset.from_asset(asset) for asset in self.assets if asset.is_available_on_date(week_day)]

    def retrieve(self, asset_code: str) -> Asset:
        asset = next((asset for asset in self.assets if asset.code == asset_code), None)
        if asset is None:
            raise ValueError(f"Asset with code {asset_code} not found")
        return asset

    def delete(self, asset_code: str) -> None:
        asset = next((asset for asset in self.assets if asset.code == asset_code), None)
        if asset is None:
            raise ValueError(f"Asset with code {asset_code} not found")
        self.assets.remove(asset)
