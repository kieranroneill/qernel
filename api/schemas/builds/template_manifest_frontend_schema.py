from pydantic import BaseModel, ConfigDict


class TemplateManifestFrontendSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    framework: str | None = None
    language: str | None = None
    package_manager: str | None = None
