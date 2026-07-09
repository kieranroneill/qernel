from pydantic import BaseModel


class BuildResolveRequestSchema(BaseModel):
    prompt: str
