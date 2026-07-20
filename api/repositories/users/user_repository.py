from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.dtos.users import UserDTO
from api.models.users import GitHubUserModel, UserModel
from api.repositories.defaults import BaseDatabaseRepository


class UserRepository(BaseDatabaseRepository[UserModel, UserDTO]):
    ##
    # private methods
    ##
    @property
    def _model_type(self) -> type[UserModel]:
        return UserModel

    def _to_model(self, dto: UserDTO) -> UserModel:
        return dto.to_model()

    async def _to_dto(self, model: UserModel) -> UserDTO:
        statement = select(UserModel).options(selectinload(UserModel.github)).where(UserModel.id == model.id)
        result = await self._database.execute(statement)
        _model = result.scalar_one()

        return UserDTO.from_model(_model)

    ##
    # public methods
    ##
    async def add(self, dto: UserDTO) -> UserDTO:
        result = await super().add(dto)

        self._logger.debug('added "%s" entry: "%s"', UserModel.__tablename__, result.id)

        return result

    async def bulk_add(self, dtos: list[UserDTO]) -> list[UserDTO]:
        results = await super().bulk_add(dtos)

        self._logger.debug(
            'added multiple "%s": %s',
            UserModel.__tablename__,
            "[" + ", ".join(f'"{result.id}"' for result in results) + "]",
        )

        return results

    async def delete_by_id(self, _id: UUID) -> bool:
        result = await super().delete_by_id(_id)

        if result:
            self._logger.debug('deleted "%s" entry: "%s"', UserModel, _id)

        return result

    async def get_by_email(self, email: str) -> UserDTO | None:
        result = await self._database.execute(
            select(UserModel).options(selectinload(UserModel.github)).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserDTO.from_model(model)

    async def get_by_github_id(self, github_id: int) -> UserDTO | None:
        result = await self._database.execute(
            select(UserModel)
            .options(selectinload(UserModel.github))
            .where(UserModel.github.has(GitHubUserModel.id == github_id))
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserDTO.from_model(model)

    async def update(self, dto: UserDTO) -> UserDTO | None:
        model = await self._database.get(self._model_type, dto.id)

        if model is None:
            return None

        model.active = dto.active
        model.display_name = dto.display_name
        model.email = dto.email
        model.github = dto.github.to_model() if dto.github else None

        try:
            await self._database.commit()
            await self._database.refresh(model)
        except Exception:
            await self._database.rollback()
            raise

        self._logger.debug('updated "%s" entry: "%s"', UserModel, model.id)

        return await self._to_dto(model)
