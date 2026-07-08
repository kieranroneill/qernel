from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AgentChatResponseDTO:
    content: str
    created_at: str
    model: str
    provider: str
    raw_response: dict[str, Any]
