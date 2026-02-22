from fastapi.testclient import TestClient

from ville_flexible.main import app


# A route that raises an exception
@app.get("/error")
async def trigger_error():
    raise Exception("Something went wrong")


client = TestClient(app, raise_server_exceptions=False)


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


def test_exception_handler():
    # Make a request to the endpoint that raises an exception
    response = client.get("/error")

    # Assert the response status code and content
    assert response.status_code == 500
    assert response.json() == {"message": "Internal Server Error"}
