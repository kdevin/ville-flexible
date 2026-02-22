import pytest
from fastapi.testclient import TestClient

from ville_flexible.asset.service import AssetService
from ville_flexible.dependencies import get_asset_service, get_activation_service
from ville_flexible.main import app

test_client = TestClient(app, raise_server_exceptions=False)


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