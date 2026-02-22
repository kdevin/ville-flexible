from fastapi.testclient import TestClient
import pytest
from ville_flexible.dependencies import assets


def test_get_assets(client: TestClient):
    # Act
    response = client.get("/assets")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == len(assets)


@pytest.mark.parametrize(
    "week_day",
    [1, 2, 3, 4, 5, 6, 7],
    ids=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)
def test_get_available_assets(client: TestClient, week_day: int):
        # Act
    response = client.get("/assets/available", params={"week_day": week_day})

    # Assert
    assert response.status_code == 200
    assert response.json() is not None
