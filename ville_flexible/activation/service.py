import logging
from abc import ABC, abstractmethod

from ville_flexible.activation.exceptions import StrategyNotCoveringRequestedVolumeException
from ville_flexible.activation.models import ActivationRequest
from ville_flexible.asset.models import AvailableAsset
from ville_flexible.asset.service import AssetService

logger = logging.getLogger(__name__)


class AbstractActivationStrategy(ABC):
    """
    Abstract base class for activation strategies.
    """

    @abstractmethod
    def select_available_assets(
        self,
        activation_request: ActivationRequest,
        available_assets: list[AvailableAsset],
    ) -> list[AvailableAsset]:
        raise NotImplementedError("Subclasses must implement this method")


class CheapestAssetCoveringRequestVolumeStrategy(AbstractActivationStrategy):
    """
    Concrete implementation of AbstractActivationStrategy that finds
    the cheapest asset's activation cost also covering the request volume.

    This algorithm is naive as it only considers assets that covers entirely the requested volume
    and does not explore all possible combinations of assets.
    """

    def select_available_assets(
        self,
        activation_request: ActivationRequest,
        available_assets: list[AvailableAsset],
    ) -> list[AvailableAsset]:
        asset_covering_requested_volume = [
            asset for asset in available_assets if asset.rate_requested_volume(activation_request.volume) >= 1
        ]

        if not asset_covering_requested_volume:
            raise StrategyNotCoveringRequestedVolumeException()

        cheapest_asset = min(asset_covering_requested_volume, key=lambda x: x.activation_cost)

        return [cheapest_asset]


class CheapestSumAssetCoveringRequestVolumeStrategy(AbstractActivationStrategy):
    """
    Concrete implementation of AbstractActivationStrategy that finds
    the cheapest sum of assets' activation cost covering the request volume.

    This algorithm is naive as it only considers assets below the requested volume per volume
    and does not explore all possible combinations of assets.
    """

    def select_available_assets(
        self,
        activation_request: ActivationRequest,
        available_assets: list[AvailableAsset],
    ) -> list[AvailableAsset]:
        asset_covering_requested_volume = [
            asset for asset in available_assets if asset.rate_requested_volume(activation_request.volume) <= 1
        ]
        assets_per_cost = sorted(asset_covering_requested_volume, key=lambda x: x.cost_per_volume)

        selected_assets = []
        for asset in assets_per_cost:
            selected_assets.append(asset)
            if sum(asset.volume for asset in selected_assets) >= activation_request.volume:
                break

        if not selected_assets or sum(asset.volume for asset in selected_assets) < activation_request.volume:
            raise StrategyNotCoveringRequestedVolumeException()

        return selected_assets


class CheapestKilowattActivationCostStrategy(AbstractActivationStrategy):
    """
    Concrete implementation of AbstractActivationStrategy that finds
    the cheapest asset's activation cost per kilowatt.

    It combines the results of CheapestAssetCoveringRequestVolumeStrategy
    and CheapestSumAssetCoveringRequestVolumeStrategy, selecting the result
    with the lowest total activation cost that also covers the requested volume.
    """

    def __init__(self):
        self.first_strategy = CheapestAssetCoveringRequestVolumeStrategy()
        self.second_strategy = CheapestSumAssetCoveringRequestVolumeStrategy()

    def select_available_assets(
        self,
        activation_request: ActivationRequest,
        available_assets: list[AvailableAsset],
    ) -> list[AvailableAsset]:

        def get_strategy_result(strategy):
            try:
                return strategy.select_available_assets(activation_request, available_assets)
            except StrategyNotCoveringRequestedVolumeException:
                return []

        first_result = get_strategy_result(self.first_strategy)
        second_result = get_strategy_result(self.second_strategy)

        first_cost = sum(asset.activation_cost for asset in first_result)
        second_cost = sum(asset.activation_cost for asset in second_result)

        if first_cost == 0 and second_cost == 0:
            raise StrategyNotCoveringRequestedVolumeException()

        if first_cost == 0:
            return second_result

        if second_cost == 0:
            return first_result

        return first_result if first_cost <= second_cost else second_result


class ActivationService:
    """
    Selects a set of available assets whose combined volumes will cover at least the requested volume.

    Attributes:
        strategy (ActivationStrategy): The strategy to be used for computing the activation list.
    """

    def __init__(self, asset_service: AssetService, strategy: AbstractActivationStrategy):
        self.asset_service = asset_service
        self.strategy = strategy

    def assets_selection(self, activation_request: ActivationRequest) -> list[AvailableAsset]:
        """
        Computes the optimal activation list based on the provided activation request and the current strategy.

        Args:
            activation_request (ActivationRequest): The request containing the date and volume for activation.
        Returns:
            list[AvailableAsset]: A list of available assets that should be activated to meet the request.
        """
        available_assets = self.asset_service.list_available(activation_request.date)

        return self.strategy.select_available_assets(activation_request, available_assets)
