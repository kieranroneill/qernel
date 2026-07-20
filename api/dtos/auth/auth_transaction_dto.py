from dataclasses import dataclass
from datetime import datetime

from api.utilities.datetime import from_iso_string, to_iso_string


@dataclass(slots=True)
class AuthTransactionDTO:
    created_at: datetime
    code_verifier: str
    id: str
    next_path: str
    state: str

    @classmethod
    def from_dict(cls, data: dict) -> "AuthTransactionDTO":
        return cls(
            id=data["id"],
            created_at=from_iso_string(data["created_at"]),
            code_verifier=data["code_verifier"],
            next_path=data["next_path"],
            state=data["state"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": to_iso_string(self.created_at),
            "code_verifier": self.code_verifier,
            "next_path": self.next_path,
            "state": self.state,
        }
