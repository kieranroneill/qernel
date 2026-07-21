from fastapi import APIRouter, Depends, status

from api.dependencies.auth import requires_authentication
from api.dtos.auth import AuthContextDTO
from api.schemas.users import UserSchema

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserSchema, status_code=status.HTTP_200_OK)
def users_me(
    auth_context: AuthContextDTO = Depends(requires_authentication),
) -> UserSchema:
    return auth_context.user.to_schema()
