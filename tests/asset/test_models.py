from pydantic import ValidationError
import pytest

from ville_flexible.asset.models import Asset, AvailableAsset


@pytest.mark.parametrize(
    "code, name, activation_cost, availability, volume",
    [
        ("A1", "Asset 1", 100.0, [1, 2, 3], 10),
        ("A2", "Asset 2", 200.0, [4, 5, 6], 20),
    ],
)
def test_asset(code, name, activation_cost, availability, volume):
    # Act
    try:
        Asset(
            code=code,
            name=name,
            activation_cost=activation_cost,
            availability=availability,
            volume=volume,
        )
    except Exception as e:
        pytest.fail(f"Asset creation failed with error: {e}")


@pytest.mark.parametrize(
    "code, name, activation_cost, availability, volume",
    [
        (123, "Asset 1", 100.0, [1, 2, 3], 10),  # Invalid code type
        ("A2", 456, 200.0, [4, 5, 6], 20),  # Invalid name type
        ("A3", "Asset 3", "invalid_cost", [1, 2, 3], 30),  # Invalid activation_cost type
        ("A4", "Asset 4", 300.0, "invalid_availability", 40),  # Invalid availability type
        ("A4", "Asset 4", 300.0, [0, 8, 9], 40),  # Invalid availability number
        ("A5", "Asset 5", 400.0, [1, 2, 3], "invalid_volume"),  # Invalid volume type
    ],
    ids=[
        "invalid code",
        "invalid name",
        "invalid activation cost",
        "invalid availability type",
        "invalid availability integers",
        "invalid volume",
    ],
)
def test_asset_invalid_data(code, name, activation_cost, availability, volume):
    # Act & Assert
    with pytest.raises((ValueError, ValidationError)):
        Asset(
            code=code,
            name=name,
            activation_cost=activation_cost,
            availability=availability,
            volume=volume,
        )


@pytest.mark.parametrize(
    "asset, expected_cost_per_volume",
    [
        (Asset(code="A1", name="Asset 1", activation_cost=100.0, availability=[1, 2, 3], volume=10), 10.0),
        (Asset(code="A2", name="Asset 2", activation_cost=200.0, availability=[4, 5, 6], volume=10), 20.0),
        (Asset(code="A3", name="Asset 3", activation_cost=300.0, availability=[7], volume=10), 30.0),
        (Asset(code="A4", name="Asset 4", activation_cost=100.0, availability=[1, 2, 3], volume=0), 0.0),
    ],
)
def test_asset_cost_per_volume(asset: Asset, expected_cost_per_volume: float):
    # Act
    cost_per_volume = asset.cost_per_volume

    # Assert
    assert cost_per_volume == expected_cost_per_volume


@pytest.mark.parametrize(
    "asset, week_day, expected_availability",
    [
        (Asset(code="A1", name="Asset 1", activation_cost=100.0, availability=[1, 2, 3], volume=10), 1, True),
        (Asset(code="A1", name="Asset 1", activation_cost=100.0, availability=[1, 2, 3], volume=10), 4, False),
        (Asset(code="A2", name="Asset 2", activation_cost=200.0, availability=[4, 5, 6, 7], volume=20), 5, True),
        (Asset(code="A2", name="Asset 2", activation_cost=200.0, availability=[4, 5, 6, 7], volume=20), 3, False),
    ],
)
def test_asset_is_available_on_date(asset: Asset, week_day: int, expected_availability: bool):
    # Act & Assert
    assert asset.is_available_on_date(week_day) is expected_availability


@pytest.mark.parametrize(
    "code, name, activation_cost, volume",
    [
        ("A1", "Asset 1", 100.0, 10),
        ("A2", "Asset 2", 200.0, 20),
    ],
)
def test_available_asset(code, name, activation_cost, volume):
    # Act
    try:
        AvailableAsset(code=code, name=name, activation_cost=activation_cost, volume=volume)
    except Exception as e:
        pytest.fail(f"AvailableAsset creation failed with error: {e}")


@pytest.mark.parametrize(
    "code, name, activation_cost, volume",
    [
        (123, "Asset 1", 100.0, 10),  # Invalid code type
        ("A2", 456, 200.0, 20),  # Invalid name type
        ("A3", "Asset 3", "invalid_cost", 30),  # Invalid activation_cost type
        ("A5", "Asset 5", 400.0, "invalid_volume"),  # Invalid volume type
    ],
    ids=["invalid code", "invalid name", "invalid activation cost", "invalid volume"],
)
def test_available_asset_invalid_data(code, name, activation_cost, volume):
    # Act & Assert
    with pytest.raises((ValueError, ValidationError)):
        AvailableAsset(code=code, name=name, activation_cost=activation_cost, volume=volume)


def test_available_asset_from_asset():
    # Arrange
    asset = Asset(code="A1", name="Asset 1", activation_cost=100.0, availability=[1, 2, 3], volume=10)

    # Act
    available_asset = AvailableAsset.from_asset(asset)

    # Assert
    assert available_asset.code == asset.code
    assert available_asset.name == asset.name
    assert available_asset.activation_cost == asset.activation_cost
    assert available_asset.volume == asset.volume


@pytest.mark.parametrize(
    "asset, requested_volume, expected_rate",
    [
        (AvailableAsset(code="A1", name="Asset 1", activation_cost=100.0, volume=10), 5, 2.0),
        (AvailableAsset(code="A2", name="Asset 2", activation_cost=200.0, volume=20), 10, 2.0),
        (AvailableAsset(code="A3", name="Asset 3", activation_cost=300.0, volume=30), 30, 1.0),
        (AvailableAsset(code="A4", name="Asset 4", activation_cost=400.0, volume=40), 50, 0.8),
        (AvailableAsset(code="A5", name="Asset 5", activation_cost=500.0, volume=0), 10, 0.0),
        (AvailableAsset(code="A6", name="Asset 6", activation_cost=600.0, volume=10), 0, 0.0),
    ],
)
def test_available_asset_rate_requested_volume(asset: AvailableAsset, requested_volume: int, expected_rate: float):
    # Act
    rate = asset.rate_requested_volume(requested_volume)

    # Assert
    assert rate == expected_rate
