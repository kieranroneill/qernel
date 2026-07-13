from test.mocks import MockAgentService

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.enums.system import ErrorCodeEnum


@pytest.fixture
def agent_service() -> MockAgentService:
    return MockAgentService()


def test_build_resolve_route_template_not_found(
    mocker,
    agent_service: MockAgentService,
) -> None:
    agent_service = MockAgentService()

    agent_service.set_chat_response("I can't help with that. Is there anything else I can assist you with?")
    mocker.patch(
        "api.routers.builds.AgentServiceFactory.create",
        return_value=agent_service,
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/builds/resolve",
            json={"prompt": "What is the meaning of life?"},
        )

    body = response.json()

    assert response.status_code == 404
    assert body["detail"]["code"] == ErrorCodeEnum.TEMPLATE_NOT_FOUND_ERROR.value


def test_build_resolve_route_success(
    mocker,
    agent_service: MockAgentService,
) -> None:
    agent_service.set_chat_response("""
Here is the extracted software project intent in JSON format:

```json
{
  "app_kind": "saas",
  "backend_framework": "fastapi",
  "frontend_framework": "nextjs"
}
```

Note: I've assumed that since you mentioned a Next.js + FastAPI SaaS app, it's likely that the authentication
preference is JWT (JSON Web Tokens) and the database is not specified, so I've left it as `none`.
If you'd like to specify a different database or authentication method, please let me know!
        """)
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
    assert body["resolution"]["templateId"] == "next-fastapi-saas"
