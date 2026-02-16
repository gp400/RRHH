import datetime
from pydantic import BaseModel

class ExperienceSchema(BaseModel):

    id: int | None
    company: str
    position: str
    description: str
    initial_date: datetime.date
    end_date: datetime.date
    wage: int
    worker_id: int | None
    state: bool