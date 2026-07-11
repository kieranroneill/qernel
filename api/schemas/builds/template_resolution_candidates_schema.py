from pydantic import BaseModel, Field


class TemplateResolutionCandidateSchema(BaseModel):
    reasons: list[str] = Field(default_factory=list)
    score: float
    template_id: str
