from ville_flexible.asset.models import Asset, AvailableAsset


class AssetService:
    def __init__(self, assets: list[Asset]):
        self.assets = assets

    def get_available_assets(self, week_day: int) -> list[AvailableAsset]:
        return [
            AvailableAsset(**asset.model_dump())
            for asset in self.assets
            if asset.is_available_on_date(week_day)
        ]
