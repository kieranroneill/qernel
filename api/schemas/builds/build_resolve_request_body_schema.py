from api.schemas.defaults import BaseSchema


class BuildResolveRequestBodySchema(BaseSchema):
    prompt: str
