import json
import re

from api.dtos.agents import AgentChatResponseDTO


def json_from_agent_response(response: AgentChatResponseDTO) -> dict | None:
    text = response.content.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```json\s*(\{.*?\}|\[.*?\])\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    return None
