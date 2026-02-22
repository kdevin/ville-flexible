from ville_flexible.activation.models import ActivationRequest
from ville_flexible.activation.service import MinimizeTotalCostStrategy, ActivationService
from ville_flexible.asset.models import Asset


def test_minimize_total_cost_strategy(activation_request: ActivationRequest, assets: list[Asset]):
    # Arrange
    strategy = MinimizeTotalCostStrategy()

    # Act
    total_cost = strategy.select_available_assets(activation_request, assets)

    # Assert
    assert total_cost is not None


def test_activation_service(activation_service: ActivationService):
    # Assert
    assert activation_service is not None


def test_assets_selection(activation_service: ActivationService, activation_request: ActivationRequest):
    # Act
    selected_assets = activation_service.assets_selection(activation_request)

    # Assert
    assert selected_assets is not None
