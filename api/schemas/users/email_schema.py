from datetime import datetime
from uuid import UUID

from api.schemas.defaults import BaseSchema


class EmailSchema(BaseSchema):
    created_at: datetime
    email: str
    id: UUID
    verified: bool
