from fastapi import Request

from api.dtos.system import SystemConfigDTO


def system_config(request: Request) -> SystemConfigDTO:
    return request.app.state.config
