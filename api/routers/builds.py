from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.controllers.builds import BuildsController
from api.dependencies.auth import requires_authentication
from api.dependencies.configs import system_config
from api.dependencies.storage import database
from api.dtos.auth import AuthContextDTO
from api.dtos.system import SystemConfigDTO
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.templates import TemplateNotFoundError
from api.schemas.builds import (
    BuildResolveRequestBodySchema,
    BuildResolveResponseBodySchema,
)
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/builds", tags=["builds"])


@router.post("/resolve", response_model=BuildResolveResponseBodySchema, status_code=status.HTTP_201_CREATED)
async def build_resolve(
    body: BuildResolveRequestBodySchema,
    auth_context: AuthContextDTO = Depends(requires_authentication),
    _database: AsyncSession = Depends(database),
    _system_config: SystemConfigDTO = Depends(system_config),
) -> BuildResolveResponseBodySchema:
    logger = get_logger()

    try:
        intent, resolution, build = await BuildsController(
            database=_database,
            logger=logger,
            model_config=_system_config.model,
            root_config=_system_config.roots,
        ).resolve(
            prompt=body.prompt,
            user=auth_context.user,
        )
    except TemplateNotFoundError:
        raise TemplateNotFoundError().to_http_exception(status_code=status.HTTP_404_NOT_FOUND)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return BuildResolveResponseBodySchema(
        build=build.to_schema(), intent=intent.to_schema(), resolution=resolution.to_schema()
    )
