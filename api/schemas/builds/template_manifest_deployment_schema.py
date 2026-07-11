from pydantic import BaseModel, ConfigDict, Field


class TemplateManifestDeploymentSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    targets: list[str] = Field(default_factory=list)
