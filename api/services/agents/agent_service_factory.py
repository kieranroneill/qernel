from api.dtos.system import ModelConfigDTO
from api.services.agents import AbstractAgentService, OllarmaAgentService


class AgentServiceFactory:
    @staticmethod
    def create(model_config: ModelConfigDTO) -> AbstractAgentService:
        if model_config.provider == "ollama":
            return OllarmaAgentService(
                api_key=model_config.api_key or None, base_url=model_config.base_url, model=model_config.model
            )

        raise ValueError(format)
