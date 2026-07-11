from typing import Iterable

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

from api.dtos.agents import AgentChatResponseDTO
from api.utilities.datetime import timestamp
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
    # public methods
    ##
    async def chat(
        self,
        messages: Iterable[
            ChatCompletionAssistantMessageParam
            | ChatCompletionDeveloperMessageParam
            | ChatCompletionFunctionMessageParam
            | ChatCompletionSystemMessageParam
            | ChatCompletionToolMessageParam
            | ChatCompletionUserMessageParam
        ],
        temperature: float = 0.1,
        response_format: ResponseFormatText | ResponseFormatJSONSchema | ResponseFormatJSONObject | Omit | None = None,
    ) -> AgentChatResponseDTO:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            response_format=response_format,
        )

        self._logger.debug(f"response: {response}")

        content = response.choices[0].message.content or ""

        return AgentChatResponseDTO(
            content=content,
            created_at=timestamp(),
            model=self.model(),
            provider=self.provider(),
            raw_response=response.model_dump(),
        )

    def provider(self) -> str:
        return "ollama"
