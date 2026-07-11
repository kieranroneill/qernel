from enum import Enum


class ErrorCodeEnum(Enum):
    # chat
    CHAT_USER_CANCELLED_ERROR = 1000
    # general
    INTERNAL_SERVER_ERROR = 5000
    # model
    MODEL_NOT_SUPPORTED_ERROR = 6000
    # templates
    TEMPLATE_NOT_FOUND_ERROR = 2000
