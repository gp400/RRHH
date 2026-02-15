from pydantic import BaseModel
from schema.competence_schema import CompetenceSchema

class WorkerCompetenceSchema(BaseModel):

    id: int | None
    worker_id: int | None
    competence_id: int | None
    state: bool

    competence: CompetenceSchema | None