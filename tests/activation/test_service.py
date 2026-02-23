import pytest

from ville_flexible.activation.models import ActivationRequest
from ville_flexible.activation.service import ActivationService, CheapestAssetCoveringRequestVolumeStrategy
from ville_flexible.asset.service import AssetService


@pytest.mark.parametrize(
    "activation_request, expected_asset_code",
    [
        (ActivationRequest(date=1, volume=5), "ASSET001"),
        (ActivationRequest(date=1, volume=10), "ASSET001"),
        (ActivationRequest(date=1, volume=20), "ASSET001"),
        (ActivationRequest(date=1, volume=30), "ASSET001"),
        (ActivationRequest(date=1, volume=50), "ASSET001"),
        (ActivationRequest(date=2, volume=10), "ASSET001"),
        (ActivationRequest(date=3, volume=25), "ASSET001"),
        (ActivationRequest(date=4, volume=30), "ASSET002"),
        (ActivationRequest(date=5, volume=18), "ASSET002"),
        (ActivationRequest(date=6, volume=25), "ASSET002"),
        (ActivationRequest(date=7, volume=5), "ASSET003"),
    ],
)
def test_minimize_total_cost_strategy(
    asset_service: AssetService, activation_request: ActivationRequest, expected_asset_code: str
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestAssetCoveringRequestVolumeStrategy()

    # Act
    selected_assets = strategy.select_available_assets(activation_request, available_assets)

    # Assert
    assert len(selected_assets) == 1

    selected_asset = selected_assets[0]
    assert selected_asset.rate_requested_volume(activation_request.volume) >= 1
    assert selected_asset.code == expected_asset_code


def test_activation_service(activation_service: ActivationService):
    # Assert
    assert activation_service is not None


def test_assets_selection(activation_service: ActivationService, activation_request: ActivationRequest):
    # Act
    selected_assets = activation_service.assets_selection(activation_request)

    # Assert
    assert selected_assets is not None
