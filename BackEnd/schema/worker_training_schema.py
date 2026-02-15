from pydantic import BaseModel
from schema.training_schema import TrainingSchema

class WorkerTrainingSchema(BaseModel):

    id: int | None
    worker_id: int | None
    training_id: int | None

    training: TrainingSchema | None