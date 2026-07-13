from enum import Enum


class ErrorCodeEnum(Enum):
    # chat
    CHAT_USER_CANCELLED_ERROR = 1000
    # general
    INTERNAL_SERVER_ERROR = 5000
    # agents
    MODEL_NOT_SUPPORTED_ERROR = 6000
    MESSAGE_ROLE_NOT_SUPPORTED_ERROR = 6001
    # templates
    TEMPLATE_NOT_FOUND_ERROR = 2000
