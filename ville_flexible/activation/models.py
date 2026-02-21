from pydantic import BaseModel


class ActivationRequest(BaseModel):
    """
    Represents a request for activation of a specific volume on a given date.

    Attributes:
        date (str): The date for which the activation is requested.
        volume (int): The volume to be activated on the specified date.
    """

    date: int
    volume: int
