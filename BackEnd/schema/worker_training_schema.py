from pydantic import BaseModel

from schema.competence_schema import CompetenceSchema
from schema.training_schema import TrainingSchema

class WorkerTrainingSchema(BaseModel):

    id: int | None
    worker_id: int | None
    training_id: int | None
    state: bool

    training: TrainingSchema | None