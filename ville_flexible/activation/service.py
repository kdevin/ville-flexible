import logging
from abc import ABC, abstractmethod

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
    """

    def select_available_assets(
        self,
        activation_request: ActivationRequest,
        available_assets: list[AvailableAsset],
    ) -> list[AvailableAsset]:
        asset_covering_requested_volume = [
            asset for asset in available_assets if asset.rate_requested_volume(activation_request.volume) >= 1
        ]
        cheapest_asset = min(asset_covering_requested_volume, key=lambda x: x.activation_cost)

        return [cheapest_asset]


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
