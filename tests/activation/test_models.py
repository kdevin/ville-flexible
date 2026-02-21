from pydantic import ValidationError
import pytest

from ville_flexible.activation.models import Asset


@pytest.mark.parametrize(
    "code, name, activation_cost, availability, volume",
    [
        ("A1", "Asset 1", 100.0, [1, 2, 3], 10),
        ("A2", "Asset 2", 200.0, [4, 5, 6], 20),
    ],
)
def test_asset(code, name, activation_cost, availability, volume):
    # Arrange

    # Act
    try:
        Asset(code=code, name=name, activation_cost=activation_cost, availability=availability, volume=volume)
    except Exception as e:
        pytest.fail(f"Asset creation failed with error: {e}")


@pytest.mark.parametrize(
    "code, name, activation_cost, availability, volume",
    [
        (123, "Asset 1", 100.0, [1, 2, 3], 10),  # Invalid code type
        ("A2", 456, 200.0, [4, 5, 6], 20),  # Invalid name type
        ("A3", "Asset 3", "invalid_cost", [7, 8, 9], 30),  # Invalid activation_cost type
        ("A4", "Asset 4", 300.0, "invalid_availability", 40),  # Invalid availability type
        ("A5", "Asset 5", 400.0, [10, 11, 12], "invalid_volume"),  # Invalid volume type
    ],
    ids=["invalid_code", "invalid_name", "invalid_activation_cost", "invalid_availability", "invalid_volume"],
)
def test_asset_invalid_data(code, name, activation_cost, availability, volume):
    # Arrange

    # Act & Assert
    with pytest.raises(ValidationError):
        Asset(code=code, name=name, activation_cost=activation_cost, availability=availability, volume=volume)