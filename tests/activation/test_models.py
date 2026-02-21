from pydantic import ValidationError
import pytest

from ville_flexible.activation.models import ActivationRequest


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
