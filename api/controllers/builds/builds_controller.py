from logging import Logger
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from api.dtos.agents import ModelConfigDTO
from api.dtos.builds import BuildDTO, TemplateIntentDTO, TemplateResolutionDTO
from api.dtos.system import RootConfigDTO
from api.errors.auth import ForbiddenError
from api.repositories.builds import BuildRepository
from api.services.agents import AgentServiceFactory
from api.services.builds import TemplateResolverService
from api.utilities.datetime import now
from api.utilities.logging import get_logger


class BuildsController:
    def __init__(
        self,
        database: AsyncSession,
        model_config: ModelConfigDTO,
        root_config: RootConfigDTO,
        logger: Logger | None = None,
    ) -> None:
        agent_service = AgentServiceFactory.create(model_config=model_config)
        _logger = logger or get_logger()

        self._build_repository = BuildRepository(database=database, logger=_logger)
        self._logger = _logger
        self._root_config = root_config
        self._template_resolver_service = TemplateResolverService(agent_service=agent_service, root_config=root_config)

    ##
    # private methods
    ##

    ##
    # public methods
    ##
    async def build_by_id(self, build_id: UUID, user_id: UUID) -> BuildDTO | None:
        build = await self._build_repository.get_by_id_with_messages(_id=build_id)

        if build is None:
            return None

        # check if the user owns the build
        if build.user_id != user_id:
            raise ForbiddenError(f'user "{str(user_id)}" does not have access to build "{str(build_id)}"')

        return build

    async def builds(self, user_id: UUID) -> list[BuildDTO]:
        return await self._build_repository.get_all_by_user_id(user_id=user_id)

    async def resolve(self, prompt: str, user_id: UUID) -> tuple[TemplateIntentDTO, TemplateResolutionDTO, BuildDTO]:
        _now = now()
        build = BuildDTO(
            active=True,
            id=uuid4(),
            created_at=_now,
            updated_at=_now,
            user_id=user_id,
        )
        intent, messages = await self._template_resolver_service.intent_from_prompt(build_id=build.id, prompt=prompt)
        template_resolution = await self._template_resolver_service.resolve_from_intent(intent=intent)

        # add message to new build
        build.messages = messages

        # add the build to the database (with the messages from the intent)
        build = await self._build_repository.add(build)

        return intent, template_resolution, build
