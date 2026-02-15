import datetime
from pydantic import BaseModel
from enums.worker_type import WorkerType
from schema.department_schema import DepartmentSchema
from schema.experience_schema import ExperienceSchema
from schema.position_schema import PositionSchema
from schema.worker_competence_schema import WorkerCompetenceSchema
from schema.worker_training_schema import WorkerTrainingSchema

class WorkerSchema(BaseModel):

    id: int | None
    identification: str
    name: str
    position_id: int
    department_id: int
    recommended_id: int | None
    wage: int
    initial_date: datetime.date | None
    type: WorkerType
    state: bool

    position: PositionSchema | None = None
    department: DepartmentSchema | None = None
    recommended: WorkerSchema | None = None

    worker_competences: list[WorkerCompetenceSchema] = []
    worker_trainings: list[WorkerTrainingSchema] = []
    experiences: list[ExperienceSchema] = []
    workers: list[WorkerSchema] = []