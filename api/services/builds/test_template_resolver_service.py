from test.mocks import MockAgentService

import pytest

from api.dtos.system import RootConfigDTO
from api.schemas.builds import TemplateIntentSchema, TemplateResolutionSchema

from .template_resolver_service import TemplateResolverService


@pytest.fixture
def service(root_config: RootConfigDTO) -> TemplateResolverService:
    return TemplateResolverService(
        agent_service=MockAgentService(),
        root_config=root_config,
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # next-fastapi-saas
        (
            TemplateIntentSchema(
                app_kind="saas",
                auth_preference="jwt",
                backend_framework="fastapi",
                deployment_target="docker-compose",
                frontend_framework="nextjs",
                missing_fields=[],
                requested_features=[],
            ),
            TemplateResolutionSchema(
                derived_variables={
                    "auth_mode": "jwt",
                    "include_billing": False,
                    "requested_features": [],
                },
                reasons=[
                    "Matched app kind.",
                    "Matched frontend framework.",
                    "Matched backend framework.",
                    "Matched auth preference.",
                    "Matched deployment target.",
                ],
                score=17.0,
                template_id="next-fastapi-saas",
            ),
        ),
    ],
)
async def test_resolve_from_intent_matches(
    service: TemplateResolverService, value: TemplateIntentSchema, expected: TemplateResolutionSchema
) -> None:
    resolution = await service.resolve_from_intent(value)

    if resolution is None:
        raise AssertionError()

    assert resolution.derived_variables == expected.derived_variables
    assert resolution.reasons == expected.reasons
    assert resolution.score == expected.score
    assert resolution.template_id == expected.template_id
