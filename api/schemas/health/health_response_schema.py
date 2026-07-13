from api.schemas.defaults import BaseSchema

from .health_model_response_schema import HealthModelResponseSchema


class HealthResponseSchema(BaseSchema):
    model: HealthModelResponseSchema | None = None
