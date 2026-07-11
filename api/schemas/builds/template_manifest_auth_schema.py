from pydantic import BaseModel, ConfigDict, Field


class TemplateManifestAuthSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    supported: list[str] = Field(default_factory=list)
