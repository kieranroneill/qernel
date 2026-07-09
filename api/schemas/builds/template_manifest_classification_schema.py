from pydantic import BaseModel, ConfigDict


class TemplateManifestClassificationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    app_kind: str | None = None
