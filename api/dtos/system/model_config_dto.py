from dataclasses import dataclass


@dataclass(slots=True)
class ModelConfigDTO:
    base_url: str
    model: str
    provider: str
