import pytest
from fastapi.testclient import TestClient

from ville_flexible.asset.service import AssetService
from ville_flexible.dependencies import get_asset_service, get_activation_service
from ville_flexible.main import app

test_client = TestClient(app)
# You can set raise_server_exceptions to False if you want to see the actual response from the server
# instead of having exceptions raised in the test client. This can be useful for debugging purposes.
# test_client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def client() -> TestClient:
    return test_client


@pytest.fixture
def assets() -> list:
    return get_asset_service().assets


@pytest.fixture
def asset_service() -> AssetService:
    return get_asset_service()


@pytest.fixture
def activation_service(asset_service: AssetService):
    return get_activation_service(asset_service=asset_service)