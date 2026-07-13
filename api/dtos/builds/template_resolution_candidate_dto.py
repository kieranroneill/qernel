from dataclasses import dataclass, field

from api.schemas.builds import TemplateResolutionCandidateSchema


@dataclass(slots=True)
class TemplateResolutionCandidateDTO:
    reasons: list[str] = field(default_factory=list)
    score: float = 0.0
    template_id: str = ""

    @classmethod
    def from_schema(
        cls,
        schema: TemplateResolutionCandidateSchema,
    ) -> "TemplateResolutionCandidateDTO":
        return cls(
            reasons=list(schema.reasons),
            score=schema.score,
            template_id=schema.template_id,
        )

    def to_schema(self) -> TemplateResolutionCandidateSchema:
        return TemplateResolutionCandidateSchema(
            reasons=list(self.reasons),
            score=self.score,
            template_id=self.template_id,
        )
