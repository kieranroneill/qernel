from enum import Enum


class BuildStageEnum(Enum):
    INITIATED = "initiated"
    PLAN = "plan"
    VALIDATE = "validate"
    READY = "ready"
