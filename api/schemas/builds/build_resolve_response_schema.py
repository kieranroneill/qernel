from pydantic import BaseModel

from .template_intent_schema import TemplateIntentSchema
from .template_resolution_schema import TemplateResolutionSchema


class BuildResolveResponseSchema(BaseModel):
    intent: TemplateIntentSchema
    resolution: TemplateResolutionSchema
