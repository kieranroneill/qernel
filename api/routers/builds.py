from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends

from api.dependencies import system_config
from api.dtos.builds import BuildDTO
from api.dtos.system import SystemConfigDTO
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.templates import TemplateNotFoundError
from api.schemas.builds import BuildResolveRequestSchema, BuildResolveResponseSchema
from api.services.agents import AgentServiceFactory
from api.services.builds import TemplateResolverService
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/builds", tags=["builds"])


@router.post("/resolve", response_model=BuildResolveResponseSchema)
async def build_resolve(
    request: BuildResolveRequestSchema,
    _system_config: SystemConfigDTO = Depends(system_config),
) -> BuildResolveResponseSchema:
    logger = get_logger()

    try:
        agent_service = AgentServiceFactory.create(model_config=_system_config.model)
        template_resolver_service = TemplateResolverService(
            agent_service=agent_service, root_config=_system_config.roots
        )
        now = datetime.now()
        build = BuildDTO(
            active=True,
            id=uuid4(),
            created_at=now,
            updated_at=now,
        )
        intent_result = await template_resolver_service.intent_from_prompt(build_id=build.id, prompt=request.prompt)
        template_resolution = await template_resolver_service.resolve_from_intent(intent=intent_result.intent)
    except TemplateNotFoundError:
        raise TemplateNotFoundError().to_http_exception(status_code=404)
    except BaseError as e:
        raise e.to_http_exception(status_code=500)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=500)

    build.messages = intent_result.messages

    return BuildResolveResponseSchema(
        build=build.to_schema(), intent=intent_result.intent.to_schema(), resolution=template_resolution.to_schema()
    )
