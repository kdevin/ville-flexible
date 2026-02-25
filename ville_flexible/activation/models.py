from pydantic import BaseModel, computed_field

from ville_flexible.asset.models import AvailableAsset


class ActivationRequest(BaseModel):
    """
    Represents a request for activation of a specific volume on a given date.

    Attributes:
        date (str): The date for which the activation is requested.
        volume (int): The volume to be activated on the specified date.
    """

    date: int
    volume: int


class ActivationResponse(BaseModel):
    """
    Represents the response for an activation request, containing the list of assets to be activated.

    Attributes:
        assets (list[AvailableAsset]): A list of available assets that should be activated to meet the request.
    """

    assets: list[AvailableAsset]

    @computed_field
    @property
    def total_activation_cost(self) -> float:
        return sum(asset.activation_cost for asset in self.assets)

    @computed_field
    @property
    def total_volume(self) -> int:
        return sum(asset.volume for asset in self.assets)
