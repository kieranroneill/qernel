from pydantic import Field

from api.schemas.defaults import BaseSchema

from .template_resolution_candidates_schema import TemplateResolutionCandidateSchema


class TemplateResolutionSchema(BaseSchema):
    candidates: list[TemplateResolutionCandidateSchema] = Field(default_factory=list)
    derived_variables: dict[str, object]
    reasons: list[str]
    score: float
    template_id: str
    unresolved_questions: list[str] = Field(default_factory=list)
