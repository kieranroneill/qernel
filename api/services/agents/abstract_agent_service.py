from abc import ABC, abstractmethod
from typing import Iterable

from openai import Omit
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


class AbstractAgentService(ABC):
    def __init__(self, api_key: str | None, base_url: str, model: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._model = model

    ##
    # public methods
    ##
    @abstractmethod
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
        pass

    def model(self) -> str:
        return self._model

    @abstractmethod
    def provider(self) -> str:
        pass
