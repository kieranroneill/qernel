from fastapi import Request

from api.dtos.auth import AuthContextDTO


def auth_context(request: Request) -> AuthContextDTO | None:
    return request.state.auth_context
