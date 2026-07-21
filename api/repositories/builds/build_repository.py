from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.dtos.builds import BuildDTO
from api.models.builds import BuildModel
from api.repositories.defaults import BaseDatabaseRepository


class BuildRepository(BaseDatabaseRepository[BuildModel, BuildDTO]):
    ##
    # private methods
    ##
    @property
    def _model_type(self) -> type[BuildModel]:
        return BuildModel

    def _to_model(self, dto: BuildDTO) -> BuildModel:
        return dto.to_model()

    async def _to_dto(self, model: BuildModel) -> BuildDTO:
        statement = select(BuildModel).where(BuildModel.id == model.id)
        result = await self._database.execute(statement)
        _model = result.scalar_one()

        return BuildDTO.from_model(_model)

    ##
    # public methods
    ##
    async def add(self, dto: BuildDTO) -> BuildDTO:
        result = await super().add(dto)

        self._logger.debug('added "%s" entry: "%s"', BuildModel.__tablename__, result.id)

        return result

    async def bulk_add(self, dtos: list[BuildDTO]) -> list[BuildDTO]:
        results = await super().bulk_add(dtos)

        self._logger.debug(
            'added multiple "%s": %s',
            BuildModel.__tablename__,
            "[" + ", ".join(f'"{result.id}"' for result in results) + "]",
        )

        return results

    async def delete_by_id(self, _id: UUID) -> bool:
        result = await super().delete_by_id(_id)

        if result:
            self._logger.debug('deleted "%s" entry: "%s"', BuildModel, _id)

        return result

    async def get_all_by_user_id(self, user_id: UUID) -> list[BuildDTO]:
        statement = select(BuildModel).where(BuildModel.user_id == user_id)
        result = await self._database.execute(statement)
        models = result.scalars().all()

        return [BuildDTO.from_model(model) for model in models]

    async def get_by_id_with_messages(self, _id: UUID) -> BuildDTO | None:
        statement = select(BuildModel).options(selectinload(BuildModel.messages)).where(BuildModel.id == _id)
        result = await self._database.execute(statement)
        model = result.scalar_one_or_none()

        return BuildDTO.from_model(model) if model else None

    async def update(self, dto: BuildDTO) -> BuildDTO | None:
        model = await self._database.get(self._model_type, dto.id)

        if model is None:
            return None

        model.active = dto.active
        model.error_message = dto.error_message
        model.extra_data = dict(dto.extra_data)
        model.internal_notes = dto.internal_notes
        model.project_name = dto.project_name
        model.resolved_variables = dict(dto.resolved_variables)
        model.selected_feature_packs = list(dto.selected_feature_packs)
        model.stage = dto.stage
        model.template_id = dto.template_id

        try:
            await self._database.commit()
            await self._database.refresh(model)
        except Exception:
            await self._database.rollback()
            raise

        self._logger.debug('updated "%s" entry: "%s"', BuildModel, model.id)

        return await self._to_dto(model)
