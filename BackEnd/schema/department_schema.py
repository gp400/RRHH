from pydantic import BaseModel

class DepartmentSchema(BaseModel):

    id: int | None
    name: str
    description: str
    state: bool