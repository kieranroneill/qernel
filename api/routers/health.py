from fastapi import APIRouter

from api.schemas.health import HealthResponseSchema

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> HealthResponseSchema:
    return HealthResponseSchema(
        model=None,
    )
