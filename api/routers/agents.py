from fastapi import APIRouter

from api.schemas.health import HealthResponseSchema

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def health() -> HealthResponseSchema:
    return HealthResponseSchema(
        model=None,
    )
