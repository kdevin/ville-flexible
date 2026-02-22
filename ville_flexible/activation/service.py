from abc import ABC, abstractmethod

from ville_flexible.activation.models import ActivationRequest
from ville_flexible.asset.models import AvailableAsset
from ville_flexible.asset.service import AssetService


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


class MinimizeTotalCostStrategy(AbstractActivationStrategy):
    """
    Concrete implementation of AbstractActivationStrategy that minimizes the total cost of activation.
    """

    def select_available_assets(
        self,
        activation_request: ActivationRequest,
        available_assets: list[AvailableAsset],
    ) -> list[AvailableAsset]:
        # TODO rate the assets based on their cost and volume
        # TODO select the ones that minimize the total cost while covering the requested volume
        raise NotImplementedError("This strategy is not yet implemented")


class ActivationService:
    """
    Selects a set of available assets whose combined volumes will cover at least the requested volume.

    Attributes:
        strategy (ActivationStrategy): The strategy to be used for computing the activation list.
    """

    def __init__(self, asset_service: AssetService, strategy: AbstractActivationStrategy = MinimizeTotalCostStrategy()):
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
        available_assets = self.asset_service.get_available_assets(activation_request.date)

        return self.strategy.select_available_assets(activation_request, available_assets)
