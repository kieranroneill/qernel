from api.schemas.defaults import BaseHTTPSchema

from .template_intent_schema import TemplateIntentSchema
from .template_resolution_schema import TemplateResolutionSchema


class BuildResolveResponseSchema(BaseHTTPSchema):
    intent: TemplateIntentSchema
    resolution: TemplateResolutionSchema
