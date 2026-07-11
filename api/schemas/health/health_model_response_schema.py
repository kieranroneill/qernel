from api.schemas.defaults import BaseHTTPSchema


class HealthModelResponseSchema(BaseHTTPSchema):
    name: str
