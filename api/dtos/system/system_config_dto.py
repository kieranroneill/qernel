from dataclasses import dataclass

from api.dtos.agents.model_config_dto import ModelConfigDTO
from api.dtos.auth.auth_config_dto import AuthConfigDTO

from .root_config_dto import RootConfigDTO


@dataclass(slots=True)
class SystemConfigDTO:
    auth: AuthConfigDTO
    model: ModelConfigDTO
    roots: RootConfigDTO
    title: str
