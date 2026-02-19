from pydantic import BaseModel
from schema.worker_schema import WorkerSchema

class UserSchema(BaseModel):

    id: int | None
    email: str
    password: str
    worker_id: int
    state: bool

    worker: WorkerSchema | None = None