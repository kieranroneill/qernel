from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseHTTPSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # serialize to camel case for json
        populate_by_name=True,  # allow both camel case and snake case for initialization
    )
