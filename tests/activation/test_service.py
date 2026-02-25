import pytest

from ville_flexible.activation.exceptions import StrategyNotCoveringRequestedVolumeException
from ville_flexible.activation.models import ActivationRequest
from ville_flexible.activation.service import (
    ActivationService,
    CheapestAssetCoveringRequestVolumeStrategy,
    CheapestKilowattActivationCostStrategy,
    CheapestSumAssetCoveringRequestVolumeStrategy,
)
from ville_flexible.asset.service import AssetService


def test_activation_service(activation_service: ActivationService):
    # Assert
    assert activation_service is not None


def test_assets_selection(activation_service: ActivationService, activation_request: ActivationRequest):
    # Act
    selected_assets = activation_service.assets_selection(activation_request)

    # Assert
    assert selected_assets is not None


@pytest.mark.parametrize(
    "activation_request, expected_activation_cost",
    [
        (ActivationRequest(date=1, volume=5), 100.0),
        (ActivationRequest(date=1, volume=10), 100.0),
        (ActivationRequest(date=1, volume=20), 100.0),
        (ActivationRequest(date=1, volume=30), 100.0),
        (ActivationRequest(date=1, volume=50), 100.0),
        (ActivationRequest(date=2, volume=10), 100.0),
        (ActivationRequest(date=3, volume=25), 100.0),
        (ActivationRequest(date=4, volume=30), 150.0),
        (ActivationRequest(date=5, volume=18), 150.0),
        (ActivationRequest(date=6, volume=25), 150.0),
        (ActivationRequest(date=7, volume=5), 200.0),
    ],
)
def test_cheapest_asset_covering_request_volume_strategy(
    asset_service: AssetService, activation_request: ActivationRequest, expected_activation_cost: int
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestAssetCoveringRequestVolumeStrategy()

    # Act
    selected_assets = strategy.select_available_assets(activation_request, available_assets)

    # Assert
    assert len(selected_assets) == 1
    assert sum(asset.activation_cost for asset in selected_assets) == expected_activation_cost


@pytest.mark.parametrize(
    "activation_request",
    [
        ActivationRequest(date=1, volume=101),
        ActivationRequest(date=2, volume=101),
        ActivationRequest(date=3, volume=101),
        ActivationRequest(date=4, volume=101),
        ActivationRequest(date=5, volume=101),
        ActivationRequest(date=6, volume=101),
        ActivationRequest(date=7, volume=101),
    ],
)
def test_cheapest_asset_covering_request_volume_strategy_exception(
    asset_service: AssetService, activation_request: ActivationRequest
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestAssetCoveringRequestVolumeStrategy()

    # Act & Assert
    with pytest.raises(StrategyNotCoveringRequestedVolumeException):
        strategy.select_available_assets(activation_request, available_assets)


@pytest.mark.parametrize(
    "activation_request, expected_length, expected_activation_cost",
    [
        (ActivationRequest(date=1, volume=50), 1, 100.0),
        (ActivationRequest(date=1, volume=101), 2, 300.0),
        (ActivationRequest(date=1, volume=149), 2, 300.0),
        (ActivationRequest(date=1, volume=150), 2, 300.0),
        (ActivationRequest(date=2, volume=150), 2, 300.0),
        (ActivationRequest(date=3, volume=150), 2, 300.0),
        (ActivationRequest(date=4, volume=150), 2, 350.0),
        (ActivationRequest(date=5, volume=150), 2, 350.0),
        (ActivationRequest(date=6, volume=150), 2, 350.0),
        (ActivationRequest(date=7, volume=100), 1, 200.0),
    ],
)
def test_cheapest_sum_asset_covering_request_volume_strategy(
    asset_service: AssetService,
    activation_request: ActivationRequest,
    expected_length: int,
    expected_activation_cost: float,
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestSumAssetCoveringRequestVolumeStrategy()

    # Act
    try:
        selected_assets = strategy.select_available_assets(activation_request, available_assets)
    except StrategyNotCoveringRequestedVolumeException:
        pytest.fail("Strategy should cover the request volume")

    # Assert
    assert len(selected_assets) == expected_length
    assert sum(asset.activation_cost for asset in selected_assets) == expected_activation_cost


@pytest.mark.parametrize(
    "activation_request",
    [
        ActivationRequest(date=1, volume=49),
        ActivationRequest(date=1, volume=51),
        ActivationRequest(date=1, volume=151),
    ],
)
def test_cheapest_sum_asset_covering_request_volume_strategy_exception(
    asset_service: AssetService, activation_request: ActivationRequest
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestSumAssetCoveringRequestVolumeStrategy()

    # Act & Assert
    with pytest.raises(StrategyNotCoveringRequestedVolumeException):
        strategy.select_available_assets(activation_request, available_assets)


@pytest.mark.parametrize(
    "activation_request, expected_length, expected_activation_cost",
    [
        (ActivationRequest(date=1, volume=49), 1, 100.0),
        (ActivationRequest(date=1, volume=50), 1, 100.0),
        (ActivationRequest(date=1, volume=51), 1, 200.0),
        (ActivationRequest(date=1, volume=101), 2, 300.0),
        (ActivationRequest(date=1, volume=149), 2, 300.0),
        (ActivationRequest(date=1, volume=150), 2, 300.0),
    ],
)
def test_cheapest_kilowatt_activation_cost_strategy(
    asset_service: AssetService,
    activation_request: ActivationRequest,
    expected_length: int,
    expected_activation_cost: float,
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestKilowattActivationCostStrategy()

    # Act
    try:
        selected_assets = strategy.select_available_assets(activation_request, available_assets)
    except StrategyNotCoveringRequestedVolumeException:
        pytest.fail("Strategy should cover the request volume")

    # Assert
    assert len(selected_assets) == expected_length
    assert sum(asset.activation_cost for asset in selected_assets) == expected_activation_cost



@pytest.mark.parametrize(
    "activation_request",
    [
        ActivationRequest(date=1, volume=151),
    ],
)
def test_cheapest_kilowatt_activation_cost_strategy_exception(
    asset_service: AssetService, activation_request: ActivationRequest
):
    # Arrange
    available_assets = asset_service.list(activation_request.date)
    strategy = CheapestKilowattActivationCostStrategy()

    # Act & Assert
    with pytest.raises(StrategyNotCoveringRequestedVolumeException):
        strategy.select_available_assets(activation_request, available_assets)