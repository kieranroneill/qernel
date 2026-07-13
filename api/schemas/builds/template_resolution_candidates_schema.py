from pydantic import Field

from api.schemas.defaults import BaseSchema


class TemplateResolutionCandidateSchema(BaseSchema):
    reasons: list[str] = Field(default_factory=list)
    score: float
    template_id: str
