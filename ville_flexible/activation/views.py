from fastapi import APIRouter

from ville_flexible.activation.models import ActivationRequest, ActivationResponse
from ville_flexible.dependencies import ActivationServiceDep

router = APIRouter(tags=["activation"], prefix="/activation")


@router.post("/", response_model=ActivationResponse)
def assets_selection(activation_request: ActivationRequest, activation_service: ActivationServiceDep):
    selected_assets = activation_service.assets_selection(activation_request)

    return ActivationResponse(assets=selected_assets)
