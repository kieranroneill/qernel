from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class AgentChatResponseDTO:
    content: str
    created_at: datetime
    model: str
    provider: str
    raw_response: dict[str, Any]
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
