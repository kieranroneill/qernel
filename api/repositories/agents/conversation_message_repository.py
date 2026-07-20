from uuid import UUID

from api.dtos.agents import ConversationMessageDTO
from api.models.agents import ConversationMessageModel
from api.repositories.defaults import BaseDatabaseRepository


class ConversationMessageRepository(BaseDatabaseRepository[ConversationMessageModel, ConversationMessageDTO]):
    ##
    # private methods
    ##
    @property
    def _model_type(self) -> type[ConversationMessageModel]:
        return ConversationMessageModel

    def _to_model(self, dto: ConversationMessageDTO) -> ConversationMessageModel:
        return dto.to_model()

    async def _to_dto(self, model: ConversationMessageModel) -> ConversationMessageDTO:
        return ConversationMessageDTO.from_model(model)

    ##
    # public methods
    ##
    async def add(self, dto: ConversationMessageDTO) -> ConversationMessageDTO:
        result = await super().add(dto)

        self._logger.debug('added "%s" entry: "%s"', ConversationMessageModel.__tablename__, result.id)

        return result

    async def bulk_add(self, dtos: list[ConversationMessageDTO]) -> list[ConversationMessageDTO]:
        results = await super().bulk_add(dtos)

        self._logger.debug(
            'added multiple "%s": %s',
            ConversationMessageModel.__tablename__,
            "[" + ", ".join(f'"{result.id}"' for result in results) + "]",
        )

        return results

    async def delete_by_id(self, _id: UUID) -> bool:
        result = await super().delete_by_id(_id)

        if result:
            self._logger.debug('deleted "%s" entry: "%s"', ConversationMessageModel, _id)

        return result

    async def update(
        self,
        dto: ConversationMessageDTO,
    ) -> ConversationMessageDTO | None:
        model = await self._session.get(self._model_type, dto.id)

        if model is None:
            return None

        model.build_id = dto.build_id
        model.content = dto.content
        model.extra_data = dict(dto.extra_data)
        model.input_tokens = dto.input_tokens
        model.internal = dto.internal
        model.model = dto.model
        model.name = dto.name
        model.output_tokens = dto.output_tokens
        model.parent_message_id = dto.parent_message_id
        model.role = dto.role
        model.sequence_number = dto.sequence_number
        model.status = dto.status
        model.total_tokens = dto.total_tokens

        try:
            await self._session.commit()
            await self._session.refresh(model)
        except Exception:
            await self._session.rollback()
            raise

        self._logger.debug('updated "%s" entry: "%s"', ConversationMessageModel, model.id)

        return await self._to_dto(model)
