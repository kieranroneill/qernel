import secrets
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from api.app import app
from api.constants import GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME
from api.enums.system import ErrorCodeEnum
from api.services.auth import GitHubOAuthService


def test_no_cookie_found() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/auth/github/complete",
            json={"code": secrets.token_urlsafe(64), "state": GitHubOAuthService.generate_state()},
        )

    body = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert body["detail"]["code"] == ErrorCodeEnum.GITHUB_OAUTH_COOKIE_NOT_FOUND_ERROR.value


def test_no_handshake_exists() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/auth/github/complete",
            json={"code": secrets.token_urlsafe(64), "state": GitHubOAuthService.generate_state()},
            cookies={GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME: str(uuid4())},
        )

    body = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert body["detail"]["code"] == ErrorCodeEnum.UNAUTHORIZED_ERROR.value
