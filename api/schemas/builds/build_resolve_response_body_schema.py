from api.schemas.defaults import BaseSchema

from .build_schema import BuildSchema
from .template_intent_schema import TemplateIntentSchema
from .template_resolution_schema import TemplateResolutionSchema


class BuildResolveResponseBodySchema(BaseSchema):
    build: BuildSchema
    intent: TemplateIntentSchema
    resolution: TemplateResolutionSchema
