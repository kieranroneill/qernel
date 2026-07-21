from fastapi import Request

from api.dtos.system import SystemConfigDTO


def system_config(request: Request) -> SystemConfigDTO:
    """Return the application system configuration from request state.

    Args:
        request (Request): The current FastAPI request.

    Returns:
        SystemConfigDTO: The application system configuration.
    """
    return request.app.state.config
