from pydantic import BaseModel, Field


class TemplateResolutionSchema(BaseModel):
    derived_variables: dict[str, object]
    reasons: list[str]
    score: float
    template_id: str
    unresolved_questions: list[str] = Field(default_factory=list)
