from dataclasses import dataclass

from .model_config_dto import ModelConfigDTO
from .root_config_dto import RootConfigDTO


@dataclass(slots=True)
class SystemConfigDTO:
    model: ModelConfigDTO
    roots: RootConfigDTO
    title: str
