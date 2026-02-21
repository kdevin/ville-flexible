from typing import Annotated

from pydantic import AfterValidator, BaseModel


def week_days(values: list[int]) -> bool:
    """
    Validates that the given values is are valid days of the week (1-7).

    Args:
        values (list[int]): The list of values to validate.
    """
    if any(not (1 <= value <= 7) for value in values):
        raise ValueError("Invalid availability: days must be between 1 and 7")

    return values


class Asset(BaseModel):
    """
    Represents an Asset that is managed by the system.

    Attributes:
        code (str): The unique code of the asset.
        name (str): The name of the asset.
        activation_cost (float): The cost to activate the asset.
        availability (list): A list of dates when the asset is available.
        volume (int): The volume of the asset.
    """

    code: str
    name: str
    activation_cost: float
    availability: Annotated[list[int], AfterValidator(week_days)]
    volume: int


class AvailableAsset(BaseModel):
    """
    Represents an available asset that is managed by the system.

    Attributes:
        code (str): The unique code of the asset.
        name (str): The name of the asset.
        activation_cost (float): The cost to activate the asset.
        volume (int): The volume of the asset.
    """

    code: str
    name: str
    activation_cost: float
    volume: int

    @staticmethod
    def from_asset(asset: Asset) -> "AvailableAsset":
        """
        Creates an AvailableAsset instance from an Asset instance.

        Args:
            asset (Asset): The Asset instance to convert.
        Returns:
            The corresponding AvailableAsset instance.
        """
        return AvailableAsset(
            code=asset.code,
            name=asset.name,
            activation_cost=asset.activation_cost,
            volume=asset.volume,
        )
