from datetime import datetime
from uuid import UUID

from pydantic import Field

from api.enums.builds import BuildStageEnum
from api.schemas.agents import ConversationMessageSchema
from api.schemas.defaults import BaseSchema


class BuildSchema(BaseSchema):
    active: bool = True
    created_at: datetime
    error_message: str | None = None
    extra_data: dict = Field(default_factory=dict)
    id: UUID
    internal_notes: str | None = None
    messages: list[ConversationMessageSchema] | None = None
    project_name: str | None = None
    resolved_variables: dict = Field(default_factory=dict)
    selected_feature_packs: list[str] = Field(default_factory=list)
    stage: BuildStageEnum = BuildStageEnum.INITIATED
    template_id: str | None = None
    updated_at: datetime
    user_id: UUID
