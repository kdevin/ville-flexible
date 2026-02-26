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


class BaseAsset(BaseModel):
    """
    Base class for assets.

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

    @property
    def cost_per_volume(self) -> float:
        """
        Computes the cost per volume unit for the asset.

        Returns:
            The cost per volume unit.
        """
        if self.volume == 0:
            return 0

        return self.activation_cost / self.volume

    def rate_requested_volume(self, requested_volume: int) -> float:
        """
        Rates the requested volume based on the current volume.

        Args:
            requested_volume (int): The requested volume.
        Returns:
            The rate of the requested volume compared to the asset's volume. \\
            A value of 1 means the asset's volume exactly matches the requested volume,
            while a value greater than 1 means the asset's volume exceeds the requested volume.
        """
        if requested_volume == 0:
            return 0

        return self.volume / requested_volume


class Asset(BaseAsset):
    """
    Represents an Asset that is managed by the system.

    Attributes:
        code (str): The unique code of the asset.
        name (str): The name of the asset.
        activation_cost (float): The cost to activate the asset.
        availability (list): A list of dates when the asset is available.
        volume (int): The volume of the asset.
    """

    availability: Annotated[list[int], AfterValidator(week_days)]

    def is_available_on_date(self, date: int) -> bool:
        """
        Checks if the asset is available on a given date.

        Args:
            date (int): The date to check for availability.
        Returns:
            True if the asset is available on the given date, False otherwise.
        """
        return date in self.availability


class AvailableAsset(BaseAsset):
    """
    Represents an available asset that is managed by the system.

    Attributes:
        code (str): The unique code of the asset.
        name (str): The name of the asset.
        activation_cost (float): The cost to activate the asset.
        volume (int): The volume of the asset.
    """

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
