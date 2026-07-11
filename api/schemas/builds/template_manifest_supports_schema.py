from pydantic import BaseModel, ConfigDict, Field


class TemplateManifestSupportsSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feature_packs: list[str] = Field(default_factory=list)
