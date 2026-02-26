from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ville_flexible.activation.models import ActivationRequest, ActivationResponse
from ville_flexible.dependencies import ActivationServiceDep

router = APIRouter(tags=["activation"], prefix="/activation")


@router.post("/", response_model=ActivationResponse)
def assets_selection(activation_request: ActivationRequest, activation_service: ActivationServiceDep):
    if activation_request.volume <= 0:
        return JSONResponse(status_code=400, content={"detail": "Requested volume should be greater than 0"})

    selected_assets = activation_service.assets_selection(activation_request)
    return ActivationResponse(assets=selected_assets)
