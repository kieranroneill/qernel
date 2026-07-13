from dataclasses import dataclass, field

from api.dtos.agents import ConversationMessageDTO

from .template_intent_dto import TemplateIntentDTO


@dataclass(slots=True)
class IntentFromPromptResultDTO:
    intent: TemplateIntentDTO
    messages: list[ConversationMessageDTO] = field(default_factory=list)
