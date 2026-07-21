from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from api.utilities.datetime import from_iso_string, to_iso_string


@dataclass(slots=True)
class SessionDTO:
    expires_at: datetime
    id: UUID
    issued_at: datetime
    user_id: UUID

    @classmethod
    def from_dict(cls, data: dict) -> "SessionDTO":
        return cls(
            expires_at=from_iso_string(data["expires_at"]),
            id=UUID(data["id"]),
            issued_at=from_iso_string(data["issued_at"]),
            user_id=UUID(data["user_id"]),
        )

    def to_dict(self) -> dict:
        return {
            "expires_at": to_iso_string(self.expires_at),
            "id": str(self.id),
            "issued_at": to_iso_string(self.issued_at),
            "user_id": str(self.user_id),
        }
