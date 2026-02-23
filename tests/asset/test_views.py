import pytest
from fastapi.testclient import TestClient

from ville_flexible.asset.models import Asset


def test_create(client: TestClient):
    # Arrange
    new_asset = {
        "code": "NEWASSET",
        "name": "New Asset",
        "availability": [1, 2, 3],
        "activation_cost": 100.0,
        "volume": 50.0,
    }

    # Act
    response = client.post("/assets/", json=new_asset)

    # Assert
    assert response.status_code == 200
    assert response.json() == new_asset


def test_create_existing_asset(client: TestClient, assets: list[Asset]):
    # Arrange

    # Act
    response = client.post("/assets/", json=assets[0].model_dump())

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": f"Asset with code {assets[0].code} already exists"}


def test_list(client: TestClient):
    # Act
    response = client.get("/assets")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "week_day",
    [1, 2, 3, 4, 5, 6, 7],
    ids=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
)
def test_list_available_assets(client: TestClient, assets: list[Asset], week_day: int):
    # Arrange
    expected_assets = [asset.model_dump() for asset in assets if asset.is_available_on_date(week_day)]

    # Act
    response = client.get("/assets", params={"week_day": week_day})

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_assets


def test_retrieve(client: TestClient, assets: list[Asset]):
    # Act
    response = client.get(f"/assets/{assets[0].code}")

    # Assert
    assert response.status_code == 200
    assert response.json() == assets[0].model_dump()


def test_retrieve_unknown_asset(client: TestClient):
    # Act
    response = client.get("/assets/unknown")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Asset with code unknown not found"}


def test_delete(client: TestClient, assets: list[Asset]):
    # Arrange
    asset_code = assets[0].code

    # Act
    response = client.delete(f"/assets/{asset_code}")

    # Assert
    assert response.status_code == 200
    assert response.json() is None

def test_delete_unknown_asset(client: TestClient, assets: list[Asset]):
    # Arrange

    # Act
    response = client.delete("/assets/unknown")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Asset with code unknown not found"}