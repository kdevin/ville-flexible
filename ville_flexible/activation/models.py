from pydantic import BaseModel

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
    Represents the response to an activation request, containing the list of assets that should be activated.

    Attributes:
        assets (list): A list of assets that should be activated to meet the request.
    """

    assets: list[AvailableAsset]
