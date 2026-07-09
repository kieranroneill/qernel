from dataclasses import dataclass


@dataclass(slots=True)
class ModelConfigDTO:
    api_key: str | None
    base_url: str
    model: str
    provider: str
