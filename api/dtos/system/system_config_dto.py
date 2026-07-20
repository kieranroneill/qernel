from dataclasses import dataclass

from .auth_config_dto import AuthConfigDTO
from .model_config_dto import ModelConfigDTO
from .root_config_dto import RootConfigDTO


@dataclass(slots=True)
class SystemConfigDTO:
    auth: AuthConfigDTO
    model: ModelConfigDTO
    roots: RootConfigDTO
    title: str
