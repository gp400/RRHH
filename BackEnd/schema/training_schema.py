import datetime
from pydantic import BaseModel
from enums.training_level import TrainingLevel


class TrainingSchema(BaseModel):

    id: int | None
    description: str
    level: TrainingLevel
    initial_date: datetime.date
    end_date: datetime.date
    institution: str
    state: bool