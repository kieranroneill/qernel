from fastapi import status
from fastapi.testclient import TestClient

from api.app import app
from api.constants import GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME


def test_success() -> None:
    with TestClient(app) as client:
        response = client.post("/api/auth/github/start")

    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.cookies.get(GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME) is not None
    assert "github.com/login/oauth/authorize" in body["authorizeUrl"]
