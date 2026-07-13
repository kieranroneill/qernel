from dataclasses import dataclass, field
from typing import Literal

from api.constants import (
    APP_KINDS,
    AUTH_PREFERENCES,
    BACKEND_FRAMEWORKS,
    DATABASES,
    DEPLOYMENT_TARGETS,
    FRONTEND_FRAMEWORKS,
)
from api.schemas.builds import TemplateIntentSchema


@dataclass(slots=True)
class TemplateIntentDTO:
    app_kind: Literal[*APP_KINDS] | None = None
    auth_preference: Literal[*AUTH_PREFERENCES] | None = None
    backend_framework: Literal[*BACKEND_FRAMEWORKS] | None = None
    confidence: float | None = None
    database: Literal[*DATABASES] | None = None
    deployment_target: Literal[*DEPLOYMENT_TARGETS] | None = None
    frontend_framework: Literal[*FRONTEND_FRAMEWORKS] | None = None
    missing_fields: list[str] = field(default_factory=list)
    requested_features: list[str] = field(default_factory=list)

    @classmethod
    def from_schema(cls, schema: TemplateIntentSchema) -> "TemplateIntentDTO":
        return cls(
            app_kind=schema.app_kind,
            auth_preference=schema.auth_preference,
            backend_framework=schema.backend_framework,
            confidence=schema.confidence,
            database=schema.database,
            deployment_target=schema.deployment_target,
            frontend_framework=schema.frontend_framework,
            missing_fields=list(schema.missing_fields),
            requested_features=list(schema.requested_features),
        )

    def to_schema(self) -> TemplateIntentSchema:
        return TemplateIntentSchema(
            app_kind=self.app_kind,
            auth_preference=self.auth_preference,
            backend_framework=self.backend_framework,
            confidence=self.confidence,
            database=self.database,
            deployment_target=self.deployment_target,
            frontend_framework=self.frontend_framework,
            missing_fields=list(self.missing_fields),
            requested_features=list(self.requested_features),
        )
