from dataclasses import dataclass, field

from api.schemas.builds import TemplateResolutionSchema

from .template_resolution_candidate_dto import TemplateResolutionCandidateDTO


@dataclass(slots=True)
class TemplateResolutionDTO:
    candidates: list[TemplateResolutionCandidateDTO] = field(default_factory=list)
    derived_variables: dict[str, object] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    score: float = 0.0
    template_id: str = ""
    unresolved_questions: list[str] = field(default_factory=list)

    @classmethod
    def from_schema(cls, schema: TemplateResolutionSchema) -> "TemplateResolutionDTO":
        return cls(
            candidates=[TemplateResolutionCandidateDTO.from_schema(candidate) for candidate in schema.candidates],
            derived_variables=dict(schema.derived_variables),
            reasons=list(schema.reasons),
            score=schema.score,
            template_id=schema.template_id,
            unresolved_questions=list(schema.unresolved_questions),
        )

    def to_schema(self) -> TemplateResolutionSchema:
        return TemplateResolutionSchema(
            candidates=[candidate.to_schema() for candidate in self.candidates],
            derived_variables=dict(self.derived_variables),
            reasons=list(self.reasons),
            score=self.score,
            template_id=self.template_id,
            unresolved_questions=list(self.unresolved_questions),
        )
