from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient):
    # Act
    response = client.get("/healthcheck")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_helloworld(client: TestClient):
    # Act
    response = client.get("/helloworld")

    # Assert
    assert response.status_code == 200
    assert response.json() == "Hello World!"
