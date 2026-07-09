from api.schemas.defaults import BaseHTTPSchema

from .health_model_response_schema import HealthModelResponseSchema


class HealthResponseSchema(BaseHTTPSchema):
    model: HealthModelResponseSchema | None = None
