from pydantic import BaseModel


class UpdateMeRequest(BaseModel):
    name: str | None
