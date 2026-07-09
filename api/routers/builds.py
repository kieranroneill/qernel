from fastapi import APIRouter, Depends

from api.dependencies import system_config
from api.dtos.system import SystemConfigDTO
from api.schemas.builds import BuildResolveRequestSchema, BuildResolveResponseSchema
from api.services.agents import AgentServiceFactory
from api.services.builds import TemplateResolverService

router = APIRouter(prefix="/builds", tags=["builds"])


@router.post("/resolve", response_model=BuildResolveResponseSchema)
async def build_resolve(
    payload: BuildResolveRequestSchema,
    _system_config: SystemConfigDTO = Depends(system_config),
) -> BuildResolveResponseSchema:
    agent_service = AgentServiceFactory.create(model_config=_system_config.model)
    template_resolver_service = TemplateResolverService(agent_service=agent_service, root_config=_system_config.roots)

    intent = await template_resolver_service.intent_from_prompt(prompt=payload.prompt)
    template_resolution = await template_resolver_service.resolve_from_intent(intent=intent)

    if template_resolution is None:
        raise ValueError("No template resolution found")

    return BuildResolveResponseSchema(intent=intent, resolution=template_resolution)
