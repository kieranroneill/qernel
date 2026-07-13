from openai import Omit
from openai.types import (
    ResponseFormatJSONObject,
    ResponseFormatJSONSchema,
    ResponseFormatText,
)

from api.dtos.agents import AgentChatResponseDTO, ConversationMessageDTO
from api.services.agents import AbstractAgentService
from api.utilities.datetime import now


class MockAgentService(AbstractAgentService):
    def __init__(self) -> None:
        super().__init__(api_key=None, base_url="http://127.0.0.1:11434", model="mocky")

        self._chat_response = None

    ##
    # public methods
    ##
    async def chat(
        self,
        messages: list[ConversationMessageDTO],
        temperature: float = 0.1,
        response_format: ResponseFormatText | ResponseFormatJSONSchema | ResponseFormatJSONObject | Omit | None = None,
    ) -> AgentChatResponseDTO:
        return AgentChatResponseDTO(
            content=self._chat_response or "I am unable to help you with that request.",
            created_at=now(),
            model=self.model(),
            provider=self.provider(),
            raw_response={},
        )

    def provider(self) -> str:
        return "qernel"

    def set_chat_response(self, chat_response: str) -> None:
        self._chat_response = chat_response
