import pytest

from ville_flexible.asset.service import AssetService


@pytest.mark.parametrize("week_day", [1, 2, 3, 4, 5, 6, 7])
def test_get_available_assets(asset_service: AssetService, week_day: int):
    # Act
    available_assets = asset_service.list(week_day)

    # Assert
    available_assets_code = [asset.code for asset in available_assets]
    filtered_assets = [asset for asset in asset_service.assets if asset.code in available_assets_code]
    filtered_assets_code = [asset.code for asset in filtered_assets]

    assert available_assets_code == filtered_assets_code
    assert all(week_day in asset.availability for asset in filtered_assets)
