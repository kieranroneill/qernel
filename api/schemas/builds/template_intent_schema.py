from typing import Literal

from pydantic import BaseModel, Field

from api.constants import (
    APP_KINDS,
    AUTH_PREFERENCES,
    BACKEND_FRAMEWORKS,
    DATABASES,
    DEPLOYMENT_TARGETS,
    FRONTEND_FRAMEWORKS,
)


class TemplateIntentSchema(BaseModel):
    app_kind: Literal[*APP_KINDS] | None = None
    auth_preference: Literal[*AUTH_PREFERENCES] | None = None
    backend_framework: Literal[*BACKEND_FRAMEWORKS] | None = None
    confidence: float | None = None
    database: Literal[*DATABASES] | None = None
    deployment_target: Literal[*DEPLOYMENT_TARGETS] | None = None
    frontend_framework: Literal[*FRONTEND_FRAMEWORKS] | None = None
    missing_fields: list[str] = Field(default_factory=list)
    requested_features: list[str] = Field(default_factory=list)
