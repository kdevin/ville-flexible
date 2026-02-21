from pydantic import BaseModel


class Asset(BaseModel):
    code: str
    name: str
    activation_cost: float
    availability: list
    volume: int
