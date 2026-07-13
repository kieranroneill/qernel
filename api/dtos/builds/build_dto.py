from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from api.dtos.agents import ConversationMessageDTO
from api.enums.builds import BuildStageEnum
from api.models.builds import BuildModel
from api.schemas.builds import BuildSchema


@dataclass(slots=True)
class BuildDTO:
    id: UUID
    active: bool
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None
    extra_data: dict = field(default_factory=dict)
    internal_notes: str | None = None
    messages: list[ConversationMessageDTO] = field(default_factory=list)
    project_name: str | None = None
    resolved_variables: dict = field(default_factory=dict)
    selected_feature_packs: list[str] = field(default_factory=list)
    stage: BuildStageEnum = BuildStageEnum.INITIATED
    template_id: str | None = None

    @classmethod
    def from_model(cls, model: BuildModel) -> "BuildDTO":
        return cls(
            id=model.id,
            active=model.active,
            created_at=model.created_at,
            stage=model.stage,
            updated_at=model.updated_at,
            error_message=model.error_message,
            extra_data=dict(model.extra_data),
            internal_notes=model.internal_notes,
            messages=[ConversationMessageDTO.from_model(message) for message in model.messages],
            project_name=model.project_name,
            resolved_variables=dict(model.resolved_variables),
            selected_feature_packs=list(model.selected_feature_packs),
            template_id=model.template_id,
        )

    def to_model(self) -> BuildModel:
        return BuildModel(
            id=self.id,
            active=self.active,
            created_at=self.created_at,
            stage=self.stage,
            updated_at=self.updated_at,
            error_message=self.error_message,
            extra_data=dict(self.extra_data),
            internal_notes=self.internal_notes,
            messages=[message.to_model() for message in self.messages],
            project_name=self.project_name,
            resolved_variables=dict(self.resolved_variables),
            selected_feature_packs=list(self.selected_feature_packs),
            template_id=self.template_id,
        )

    @classmethod
    def from_schema(cls, schema: BuildSchema) -> "BuildDTO":
        return cls(
            id=schema.id,
            active=schema.active,
            created_at=schema.created_at,
            stage=schema.stage,
            updated_at=schema.updated_at,
            error_message=schema.error_message,
            extra_data=dict(schema.extra_data),
            internal_notes=schema.internal_notes,
            messages=[ConversationMessageDTO.from_schema(message) for message in schema.messages],
            project_name=schema.project_name,
            resolved_variables=dict(schema.resolved_variables),
            selected_feature_packs=list(schema.selected_feature_packs),
            template_id=schema.template_id,
        )

    def to_schema(self) -> BuildSchema:
        return BuildSchema(
            id=self.id,
            active=self.active,
            created_at=self.created_at,
            stage=self.stage,
            updated_at=self.updated_at,
            error_message=self.error_message,
            extra_data=dict(self.extra_data),
            internal_notes=self.internal_notes,
            messages=[message.to_schema() for message in self.messages],
            project_name=self.project_name,
            resolved_variables=dict(self.resolved_variables),
            selected_feature_packs=list(self.selected_feature_packs),
            template_id=self.template_id,
        )
