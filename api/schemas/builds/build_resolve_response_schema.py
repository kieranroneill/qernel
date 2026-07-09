from pydantic import BaseModel

from api.schemas.builds import TemplateIntentSchema, TemplateResolutionSchema


class BuildResolveResponseSchema(BaseModel):
    intent: TemplateIntentSchema
    resolution: TemplateResolutionSchema
