import os

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import system_config
from api.dtos.system import SystemConfigDTO
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.templates import TemplateNotFoundError
from api.schemas.builds import BuildResolveRequestSchema, BuildResolveResponseSchema
from api.services.agents import AgentServiceFactory
from api.services.builds import TemplateResolverService
from api.utilities.logging import get_logger

router = APIRouter(prefix="/builds", tags=["builds"])


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
        intent = await template_resolver_service.intent_from_prompt(prompt=request.prompt)
        template_resolution = await template_resolver_service.resolve_from_intent(intent=intent)
    except TemplateNotFoundError:
        raise TemplateNotFoundError().to_http_exception(status_code=404)
    except BaseError as e:
        raise e.to_http_exception(status_code=500)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=500)

    return BuildResolveResponseSchema(intent=intent, resolution=template_resolution)
