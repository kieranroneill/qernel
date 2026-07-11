from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TemplateManifestVariableSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    type: str
    required: bool = False
    values: list[str] = Field(default_factory=list)
    default: Any | None = None
