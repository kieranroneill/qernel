from dataclasses import dataclass
from datetime import datetime

from api.utilities.datetime import from_iso_string, to_iso_string


@dataclass(slots=True)
class GitHubOAuthHandshakeDTO:
    created_at: datetime
    code_verifier: str
    id: str
    state: str

    @classmethod
    def from_dict(cls, data: dict) -> "GitHubOAuthHandshakeDTO":
        return cls(
            id=data["id"],
            created_at=from_iso_string(data["created_at"]),
            code_verifier=data["code_verifier"],
            state=data["state"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": to_iso_string(self.created_at),
            "code_verifier": self.code_verifier,
            "state": self.state,
        }
