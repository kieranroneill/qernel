from pydantic import BaseModel, ConfigDict

from .template_manifest_auth_schema import TemplateManifestAuthSchema
from .template_manifest_backend_schema import TemplateManifestBackendSchema
from .template_manifest_database_schema import TemplateManifestDatabaseSchema
from .template_manifest_deployment_schema import TemplateManifestDeploymentSchema
from .template_manifest_frontend_schema import TemplateManifestFrontendSchema


class TemplateManifestStackSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    frontend: TemplateManifestFrontendSchema | None = None
    backend: TemplateManifestBackendSchema | None = None
    database: TemplateManifestDatabaseSchema | None = None
    auth: TemplateManifestAuthSchema | None = None
    deployment: TemplateManifestDeploymentSchema | None = None
