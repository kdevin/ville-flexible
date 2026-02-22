import pytest

from ville_flexible.activation.models import ActivationRequest
from ville_flexible.activation.service import ActivationService, CheapestAssetCoveringRequestVolumeStrategy
from ville_flexible.asset.models import Asset


@pytest.mark.parametrize(
    "activation_request, expected_asset_code",
    [
        (ActivationRequest(date=1, volume=5), "FAN025"),
        (ActivationRequest(date=1, volume=10), "FAN020"),
        (ActivationRequest(date=1, volume=20), "WEL031"),
        (ActivationRequest(date=1, volume=30), "MIX029"),
        (ActivationRequest(date=1, volume=50), "PMP016"),
        (ActivationRequest(date=2, volume=10), "FAN020"),
        (ActivationRequest(date=3, volume=25), "MTR022"),
        (ActivationRequest(date=4, volume=30), "MIX029"),
        (ActivationRequest(date=5, volume=18), "WEL011"),
        (ActivationRequest(date=6, volume=25), "MTR022"),
        (ActivationRequest(date=7, volume=5), "FAN025"),
    ],
)
def test_minimize_total_cost_strategy(
    assets: list[Asset], activation_request: ActivationRequest, expected_asset_code: str
):
    # Arrange
    strategy = CheapestAssetCoveringRequestVolumeStrategy()

    # Act
    selected_assets = strategy.select_available_assets(activation_request, assets)

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
