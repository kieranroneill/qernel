from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class AgentChatResponseDTO:
    content: str
    created_at: datetime
    input_tokens: int | None
    model: str
    output_tokens: int | None
    provider: str
    raw_response: dict[str, Any]
    total_tokens: int | None
