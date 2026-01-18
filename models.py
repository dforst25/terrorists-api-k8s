from pydantic import BaseModel, Field
from typing import Annotated


class TerroristModel(BaseModel):
    name: str
    location: str
    rate_danger: Annotated[int, Field(ge=1, le=10)]
