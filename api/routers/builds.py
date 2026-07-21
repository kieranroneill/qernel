from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.configs import system_config
from api.dependencies.storage import database
from api.dtos.builds import BuildDTO
from api.dtos.system import SystemConfigDTO
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.templates import TemplateNotFoundError
from api.repositories.builds import BuildRepository
from api.schemas.builds import (
    BuildResolveRequestBodySchema,
    BuildResolveResponseBodySchema,
)
from api.services.agents import AgentServiceFactory
from api.services.builds import TemplateResolverService
from api.utilities.datetime import now
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/builds", tags=["builds"])


@router.post("/resolve", response_model=BuildResolveResponseBodySchema)
async def build_resolve(
    body: BuildResolveRequestBodySchema,
    _database: AsyncSession = Depends(database),
    _system_config: SystemConfigDTO = Depends(system_config),
) -> BuildResolveResponseBodySchema:
    logger = get_logger()

    try:
        agent_service = AgentServiceFactory.create(model_config=_system_config.model)
        template_resolver_service = TemplateResolverService(
            agent_service=agent_service, root_config=_system_config.roots
        )
        _now = now()
        build = BuildDTO(
            active=True,
            id=uuid4(),
            created_at=_now,
            updated_at=_now,
        )
        intent_result = await template_resolver_service.intent_from_prompt(build_id=build.id, prompt=body.prompt)
        template_resolution = await template_resolver_service.resolve_from_intent(intent=intent_result.intent)
    except TemplateNotFoundError:
        raise TemplateNotFoundError().to_http_exception(status_code=status.HTTP_404_NOT_FOUND)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # add message to new build
    build.messages = intent_result.messages

    # add the build to the database (with the messages from the intent)
    build = await BuildRepository(logger=logger, database=_database).add(build)

    return BuildResolveResponseBodySchema(
        build=build.to_schema(), intent=intent_result.intent.to_schema(), resolution=template_resolution.to_schema()
    )
