from api.schemas.defaults import BaseHTTPSchema


class BuildResolveRequestSchema(BaseHTTPSchema):
    prompt: str
