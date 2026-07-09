from pydantic import BaseModel, ConfigDict, Field


class TemplateManifestDatabaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    default: str | None = None
    supported: list[str] = Field(default_factory=list)
