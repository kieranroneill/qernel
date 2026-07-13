from datetime import datetime

from openai import AsyncOpenAI, Omit
from openai.types import (
    ResponseFormatJSONObject,
    ResponseFormatJSONSchema,
    ResponseFormatText,
)
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionDeveloperMessageParam,
    ChatCompletionFunctionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)

from api.dtos.agents import AgentChatResponseDTO, ConversationMessageDTO
from api.enums.agents import MessageRoleEnum
from api.utilities.logging import get_logger

from .abstract_agent_service import AbstractAgentService


class OllamaAgentService(AbstractAgentService):
    def __init__(self, api_key: str | None, base_url: str, model: str) -> None:
        super().__init__(api_key, base_url, model)

        self._client = AsyncOpenAI(
            api_key=self._api_key or "ollama",
            base_url=f"{base_url}/v1/",
        )
        self._logger = get_logger()

    ##
    # private methods
    ##
    def _to_openai_message(
        self, message: ConversationMessageDTO
    ) -> (
        ChatCompletionAssistantMessageParam
        | ChatCompletionDeveloperMessageParam
        | ChatCompletionFunctionMessageParam
        | ChatCompletionSystemMessageParam
        | ChatCompletionToolMessageParam
        | ChatCompletionUserMessageParam
    ):
        match message.role:
            case MessageRoleEnum.ASSISTANT:
                return ChatCompletionAssistantMessageParam(
                    content=message.content,
                    role="assistant",
                )
            case MessageRoleEnum.SYSTEM:
                return ChatCompletionSystemMessageParam(
                    content=message.content,
                    role="system",
                )
            case MessageRoleEnum.USER:
                return ChatCompletionUserMessageParam(
                    content=message.content,
                    role="user",
                )

    ##
    # public methods
    ##
    async def chat(
        self,
        messages: list[ConversationMessageDTO],
        temperature: float = 0.1,
        response_format: ResponseFormatText | ResponseFormatJSONSchema | ResponseFormatJSONObject | Omit | None = None,
    ) -> AgentChatResponseDTO:
        _messages = [self._to_openai_message(m) for m in messages]
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=_messages,
            temperature=temperature,
            response_format=response_format,
        )

        self._logger.debug(f"response: {response.model_dump()}")

        content = response.choices[0].message.content or ""

        return AgentChatResponseDTO(
            content=content,
            created_at=datetime.fromtimestamp(response.created),
            input_tokens=response.usage.prompt_tokens,
            model=self.model(),
            output_tokens=response.usage.completion_tokens,
            provider=self.provider(),
            raw_response=response.model_dump(),
            total_tokens=response.usage.total_tokens,
        )

    def provider(self) -> str:
        return "ollama"
