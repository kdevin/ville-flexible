from fastapi.testclient import TestClient

from ville_flexible.activation.models import ActivationRequest


def test_assets_selection(client: TestClient, activation_request: ActivationRequest):
    # Act
    response = client.post("/activation", json=activation_request.model_dump())

    # Assert
    assert response.status_code == 200
    assert len(response.json()) is not None


def test_assets_selection_400(client: TestClient):
    # Act
    response = client.post("/activation", json=ActivationRequest(date=1, volume=0).model_dump())

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Requested volume should be greater than 0"}
