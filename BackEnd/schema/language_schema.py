from pydantic import BaseModel

class LanguageSchema(BaseModel):

    id: int | None
    name: str
    state: bool