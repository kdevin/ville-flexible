from fastapi import APIRouter

from ville_flexible.activation.models import ActivationRequest
from ville_flexible.asset.models import AvailableAsset
from ville_flexible.dependencies import ActivationServiceDep

router = APIRouter(tags=["activation"], prefix="/activation")


@router.post("/", response_model=list[AvailableAsset])
def assets_selection(activation_request: ActivationRequest, activation_service: ActivationServiceDep):
    return activation_service.assets_selection(activation_request)
