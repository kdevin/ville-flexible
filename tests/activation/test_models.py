from pydantic import ValidationError
import pytest

from ville_flexible.activation.models import ActivationRequest, ActivationResponse
from ville_flexible.asset.models import Asset, AvailableAsset


@pytest.mark.parametrize(
    "date, volume",
    [
        (1, 100),
        (2, 200),
    ],
)
def test_activation_request(date: int, volume: int):
    # Act
    try:
        ActivationRequest(date=date, volume=volume)
    except Exception as e:
        pytest.fail(f"ActivationRequest creation failed with error: {e}")


@pytest.mark.parametrize(
    "date, volume",
    [
        ("invalid_date", 100),  # Invalid date type
        (1, "invalid_volume"),  # Invalid volume type
    ],
    ids=["invalid date", "invalid volume"],
)
def test_activation_request_invalid_data(date: int, volume: int):
    # Act
    with pytest.raises((ValueError, ValidationError)):
        ActivationRequest(date=date, volume=volume)


@pytest.mark.parametrize(
    "available_assets",
    [
        [],
        [
            AvailableAsset(code="A1", name="Asset 1", activation_cost=100.0, volume=10),
        ],
        [
            AvailableAsset(code="A2", name="Asset 2", activation_cost=200.0, volume=20),
            AvailableAsset(code="A3", name="Asset 3", activation_cost=300.0, volume=30),
        ],
    ],
)
def test_activation_response(available_assets: list[AvailableAsset]):
    # Act
    try:
        ActivationResponse(assets=available_assets)
    except Exception as e:
        pytest.fail(f"ActivationResponse creation failed with error: {e}")


@pytest.mark.parametrize(
    "available_assets",
    [
        [1, 2],
        ["1", "2"],
        [
            Asset(code="A1", name="Asset 1", activation_cost=100.0, availability=[1, 2, 3], volume=10),
            Asset(code="A2", name="Asset 2", activation_cost=200.0, availability=[1, 2, 3], volume=20),
        ],
    ],
)
def test_activation_response_invalid_data(available_assets: list[AvailableAsset]):
    # Act
    with pytest.raises((ValueError, ValidationError)):
        ActivationResponse(assets=available_assets)
