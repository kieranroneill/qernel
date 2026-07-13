import logging

from api.dtos.system import ModelConfigDTO
from api.errors.agents import ModelNotSupportedError

from .abstract_agent_service import AbstractAgentService
from .ollama_agent_service import OllamaAgentService


class AgentServiceFactory:
    @staticmethod
    def create(model_config: ModelConfigDTO) -> AbstractAgentService:
        if model_config.provider == "ollama":
            return OllamaAgentService(
                api_key=model_config.api_key or None, base_url=model_config.base_url, model=model_config.model
            )

        logging.debug(f'unknown provider "{model_config.provider}"')

        raise ModelNotSupportedError(provider=model_config.provider)
