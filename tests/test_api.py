from fastapi.testclient import TestClient

from ville_flexible.main import app
from ville_flexible.activation.exceptions import StrategyNotCoveringRequestedVolumeException


# A route that raises an exception
@app.get("/error")
async def trigger_error():
    raise Exception("Something went wrong")


# A route that raises an exception
@app.get("/strategy_not_covering_requested_volume")
async def trigger_strategy():
    raise StrategyNotCoveringRequestedVolumeException()


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


def test_exception_handler(client: TestClient):
    # Make a request to the endpoint that raises an exception
    response = client.get("/error")

    # Assert the response status code and content
    assert response.status_code == 500
    assert response.json() == {"message": "Internal Server Error"}


def test_strategy_not_covering_requested_volume_exception_handler(client: TestClient):
    # Make a request to the endpoint that raises an exception
    response = client.get("/strategy_not_covering_requested_volume")

    # Assert the response status code and content
    assert response.status_code == 422
    assert response.json() == {"message": StrategyNotCoveringRequestedVolumeException.MESSAGE}
