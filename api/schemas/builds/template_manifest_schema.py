from pydantic import BaseModel, ConfigDict, Field

from .template_manifest_classification_schema import (
    TemplateManifestClassificationSchema,
)
from .template_manifest_stack_schema import TemplateManifestStackSchema
from .template_manifest_supports_schema import TemplateManifestSupportsSchema
from .template_manifest_variable_schema import TemplateManifestVariableSchema


class TemplateManifestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    version: str
    description: str
    classification: TemplateManifestClassificationSchema | None = None
    stack: TemplateManifestStackSchema
    variables: list[TemplateManifestVariableSchema] = Field(default_factory=list)
    supports: TemplateManifestSupportsSchema | None = None
