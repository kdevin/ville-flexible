import pytest

from ville_flexible.asset.service import AssetService
from ville_flexible.config import Settings
from ville_flexible.dependencies import get_assets_from_db, get_activation_service
from ville_flexible.activation.service import CheapestAssetCoveringRequestVolumeStrategy


def test_get_assets_from_db():
    # Act
    assets = get_assets_from_db()

    # Assert
    assert assets is not None


@pytest.mark.parametrize(
    "strategy, strategy_class",
    [
        (
            "cheapest_asset_covering_request_volume",
            CheapestAssetCoveringRequestVolumeStrategy,
        )
    ],
    ids=["CheapestAssetCoveringRequestVolumeStrategy"],
)
def test_get_activation_service(asset_service: AssetService, strategy: str, strategy_class: type):
    # Arrange
    settings = Settings(strategy=strategy)

    # Act
    activation_service = get_activation_service(settings, asset_service)

    # Assert
    assert activation_service is not None
    assert isinstance(activation_service.strategy, strategy_class)


def test_get_activation_service_value_error(asset_service: AssetService):
    # Arrange
    settings = Settings(strategy="unknown")

    # Act & Assert
    with pytest.raises(ValueError):
        get_activation_service(settings, asset_service)
