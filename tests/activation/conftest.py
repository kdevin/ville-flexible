import pytest

from ville_flexible.activation.models import ActivationRequest


@pytest.fixture
def activation_request():
    return ActivationRequest(date=1, volume=100)
