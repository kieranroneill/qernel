from test.mocks import MockAgentService

import pytest
from fastapi.testclient import TestClient

from api.app import app


@pytest.fixture
def agent_service() -> MockAgentService:
    return MockAgentService()


def test_build_resolve_route(
    mocker,
) -> None:
    agent_service = MockAgentService()

    agent_service.set_chat_response(
        'Here is the extracted software project intent in JSON format:\n\n```json\n{\n  "app_kind": "saas",\n  "backend_framework": "fastapi",\n  "frontend_framework": "nextjs"\n}\n```\n\nNote: I\'ve assumed that since you mentioned a Next.js + FastAPI SaaS app, it\'s likely that the authentication preference is JWT (JSON Web Tokens) and the database is not specified, so I\'ve left it as `none`. If you\'d like to specify a different database or authentication method, please let me know!'
    )
    mocker.patch(
        "api.routers.builds.AgentServiceFactory.create",
        return_value=agent_service,
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/builds/resolve",
            json={"prompt": "Build me a Next.js + FastAPI SaaS app"},
        )

    body = response.json()

    assert response.status_code == 200
    assert body["resolution"]["template_id"] == "next-fastapi-saas"
