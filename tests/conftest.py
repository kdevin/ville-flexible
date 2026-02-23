import pytest
from fastapi.testclient import TestClient

from ville_flexible.asset.models import Asset
from ville_flexible.asset.service import AssetService
from ville_flexible.config import Settings
from ville_flexible.dependencies import get_asset_service, get_activation_service, get_assets_from_db, get_settings
from ville_flexible.main import app


@pytest.fixture
def assets() -> list[Asset]:
    return [
        Asset(
            code="ASSET001",
            name="Asset 1",
            availability=[1, 2, 3],
            activation_cost=100.0,
            volume=50.0,
        ),
        Asset(
            code="ASSET002",
            name="Asset 2",
            availability=[4, 5, 6],
            activation_cost=150.0,
            volume=75.0,
        ),
        Asset(
            code="ASSET003",
            name="Asset 3",
            availability=[1, 2, 3, 4, 5, 6, 7],
            activation_cost=200.0,
            volume=100.0,
        ),
    ]


@pytest.fixture
def client(assets: list[Asset]):
    def override_assets():
        return assets

    app.dependency_overrides[get_assets_from_db] = override_assets
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides = {}


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def asset_service(assets: list[Asset]) -> AssetService:
    return get_asset_service(assets)


@pytest.fixture
def activation_service(settings: Settings, asset_service: AssetService):
    return get_activation_service(settings=settings, asset_service=asset_service)
