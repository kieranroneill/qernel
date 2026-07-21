from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.controllers.builds import BuildsController
from api.dependencies.auth import requires_authentication
from api.dependencies.configs import system_config
from api.dependencies.storage import database
from api.dtos.auth import AuthContextDTO
from api.dtos.system import SystemConfigDTO
from api.errors.auth import ForbiddenError
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.templates import TemplateNotFoundError
from api.schemas.builds import (
    BuildResolveRequestBodySchema,
    BuildResolveResponseBodySchema,
    BuildSchema,
)
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/builds", tags=["builds"])


@router.get("", response_model=list[BuildSchema], status_code=status.HTTP_200_OK)
async def builds(
    auth_context: AuthContextDTO = Depends(requires_authentication),
    _database: AsyncSession = Depends(database),
    _system_config: SystemConfigDTO = Depends(system_config),
) -> list[BuildSchema]:
    logger = get_logger()
    controller = BuildsController(
        database=_database,
        logger=logger,
        model_config=_system_config.model,
        root_config=_system_config.roots,
    )

    try:
        _builds = await controller.builds(user_id=auth_context.user.id)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return [build.to_schema() for build in _builds]


@router.get("/{build_id}", response_model=BuildSchema, status_code=status.HTTP_200_OK)
async def build_by_id(
    build_id: str,
    auth_context: AuthContextDTO = Depends(requires_authentication),
    _database: AsyncSession = Depends(database),
    _system_config: SystemConfigDTO = Depends(system_config),
) -> BuildSchema:
    logger = get_logger()
    controller = BuildsController(
        database=_database,
        logger=logger,
        model_config=_system_config.model,
        root_config=_system_config.roots,
    )

    try:
        build = await controller.build_by_id(build_id=UUID(build_id), user_id=auth_context.user.id)
    except ForbiddenError:
        raise ForbiddenError().to_http_exception(status_code=status.HTTP_403_FORBIDDEN)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if build is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return build.to_schema()


@router.post("/resolve", response_model=BuildResolveResponseBodySchema, status_code=status.HTTP_201_CREATED)
async def builds_resolve(
    body: BuildResolveRequestBodySchema,
    auth_context: AuthContextDTO = Depends(requires_authentication),
    _database: AsyncSession = Depends(database),
    _system_config: SystemConfigDTO = Depends(system_config),
) -> BuildResolveResponseBodySchema:
    logger = get_logger()
    controller = BuildsController(
        database=_database,
        logger=logger,
        model_config=_system_config.model,
        root_config=_system_config.roots,
    )

    try:
        intent, resolution, build = await controller.resolve(
            prompt=body.prompt,
            user_id=auth_context.user.id,
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
