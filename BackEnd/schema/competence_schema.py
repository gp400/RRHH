from pydantic import BaseModel

class CompetenceSchema(BaseModel):

    id: int | None
    name: str
    description: str
    state: bool