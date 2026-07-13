from enum import Enum


class MessageStatusEnum(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
