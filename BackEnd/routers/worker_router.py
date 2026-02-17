from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models.competence import Competence
from db.models.experience import Experience
from db.models.training import Training
from db.models.worker import Worker
from db.models.worker_competence import WorkerCompetence
from db.models.worker_training import WorkerTraining
from enums.position_risk_level import PositionRiskLevel
from enums.training_level import TrainingLevel
from enums.worker_type import WorkerType
from schema.competence_schema import CompetenceSchema
from schema.department_schema import DepartmentSchema
from schema.experience_schema import ExperienceSchema
from schema.position_schema import PositionSchema
from schema.training_schema import TrainingSchema
from schema.worker_competence_schema import WorkerCompetenceSchema
from schema.worker_schema import WorkerSchema
from schema.worker_training_schema import WorkerTrainingSchema

router = APIRouter()

not_found_message_employee = "Empleado no encontrado."
not_found_message_candidate = "Candidato no encontrado."
recommended_message = "El Empleado no se puede eliminar porque posee Candidatos relacionados."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all/{workerType}")
def get_all(
        workerType: int,
        position_id: Optional[int] = None,
        competence_id: Optional[int] = None,
        training_id: Optional[int] = None,
        db: Session = Depends(get_db)):

    query = (db.query(Worker)
            .join(WorkerCompetence, Worker.id == WorkerCompetence.worker_id)
            .join(Competence, WorkerCompetence.competence_id == Competence.id)
            .join(WorkerTraining, Worker.id == WorkerTraining.worker_id)
            .join(Training, WorkerTraining.training_id == Training.id)
            .filter(Worker.state, Worker.type == workerType))

    if position_id is not None:
        query = query.filter(Worker.position_id == position_id)

    if competence_id is not None:
        query = query.filter(Competence.id == competence_id)

    if training_id is not None:
        query = query.filter(Training.id == training_id)

    workers: list[type[Worker]] = query.all()

    return list(map(lambda worker: WorkerSchema(
        id=worker.id,
        identification=worker.identification,
        name=worker.name,
        position_id=worker.position_id,
        department_id=worker.department_id,
        recommended_id=worker.recommended_id,
        wage=worker.wage,
        initial_date=worker.initial_date,
        type=WorkerType(worker.type),
        position=PositionSchema(
            id=worker.position.id,
            name=worker.position.name,
            risk_level=PositionRiskLevel(worker.position.risk_level),
            min_wage=worker.position.min_wage,
            max_wage=worker.position.max_wage,
            state=worker.position.state
        ),
        department=DepartmentSchema(id=worker.department.id, name=worker.department.name, description=worker.department.description, state=worker.department.state),
        recommended=None if worker.recommended is None else WorkerSchema(
            id=worker.recommended.id,
            identification=worker.recommended.identification,
            name=worker.recommended.name,
            position_id=worker.recommended.position_id,
            department_id=worker.recommended.department_id,
            recommended_id=worker.recommended.recommended_id,
            wage=worker.recommended.wage,
            initial_date=worker.recommended.initial_date,
            type=WorkerType(worker.recommended.type),
            state=worker.recommended.state
        ),
        worker_competences=list(map(lambda wc: WorkerCompetenceSchema(id=wc.id, worker_id=wc.worker_id, competence_id=wc.competence_id, state=wc.state, competence=CompetenceSchema(id=wc.competence.id, name=wc.competence.name, description=wc.competence.description, state=wc.competence.state)), worker.worker_competences)),
        worker_trainings=list(map(lambda wt: WorkerTrainingSchema(id=wt.id, worker_id=wt.worker_id, training_id=wt.training_id, state=wt.state, training=TrainingSchema(
            id=wt.training.id,
            description=wt.training.description,
            level=TrainingLevel(wt.training.level),
            initial_date=wt.training.initial_date,
            end_date=wt.training.end_date,
            institution=wt.training.institution,
            state=wt.training.state,
        )), worker.worker_trainings)),
        experiences=list(map(lambda e: ExperienceSchema(id=e.id, company=e.company, position=e.position, description=e.description, initial_date=e.initial_date, end_date=e.end_date, wage=e.wage, worker_id=e.worker_id, state=e.state), worker.experiences)),
        state=worker.state,
    ), workers))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    worker_db: type[Worker] = db.query(Worker).filter(Worker.id == id).first()

    if worker_db is None:
        raise HTTPException(status_code=404, detail=not_found_message_candidate)

    return WorkerSchema(
        id=worker_db.id,
        identification=worker_db.identification,
        name=worker_db.name,
        position_id=worker_db.position_id,
        department_id=worker_db.department_id,
        recommended_id=worker_db.recommended_id,
        wage=worker_db.wage,
        initial_date=worker_db.initial_date,
        type=WorkerType(worker_db.type),
        position=PositionSchema(
            id=worker_db.position.id,
            name=worker_db.position.name,
            risk_level=PositionRiskLevel(worker_db.position.risk_level),
            min_wage=worker_db.position.min_wage,
            max_wage=worker_db.position.max_wage,
            state=worker_db.position.state
        ),
        department=DepartmentSchema(id=worker_db.department.id, name=worker_db.department.name,
                                    description=worker_db.department.description, state=worker_db.department.state),
        recommended=None if worker_db.recommended is None else WorkerSchema(
            id=worker_db.recommended.id,
            identification=worker_db.recommended.identification,
            name=worker_db.recommended.name,
            position_id=worker_db.recommended.position_id,
            department_id=worker_db.recommended.department_id,
            recommended_id=worker_db.recommended.recommended_id,
            wage=worker_db.recommended.wage,
            initial_date=worker_db.recommended.initial_date,
            type=WorkerType(worker_db.recommended.type),
            state=worker_db.recommended.state
        ),
        worker_competences=list(map(lambda wc: WorkerCompetenceSchema(id=wc.id, worker_id=wc.worker_id, competence_id=wc.competence_id, state=wc.state, competence=CompetenceSchema(id=wc.competence.id, name=wc.competence.name, description=wc.competence.description, state=wc.competence.state)), worker_db.worker_competences)),
        worker_trainings=list(map(lambda wt: WorkerTrainingSchema(id=wt.id, worker_id=wt.worker_id, training_id=wt.training_id, state=wt.state, training=TrainingSchema(
            id=wt.training.id,
            description=wt.training.description,
            level=TrainingLevel(wt.training.level),
            initial_date=wt.training.initial_date,
            end_date=wt.training.end_date,
            institution=wt.training.institution,
            state=wt.training.state,
        )), worker_db.worker_trainings)),
        experiences=list(map(lambda e: ExperienceSchema(id=e.id, company=e.company, position=e.position, description=e.description, initial_date=e.initial_date, end_date=e.end_date, wage=e.wage, worker_id=e.worker_id, state=e.state), worker_db.experiences)),
        state=worker_db.state,
    )

@router.post("/create", status_code=201)
def create(worker: WorkerSchema, db: Session = Depends(get_db)):

    for competence in worker.worker_competences:
        competence.state = True

    for training in worker.worker_trainings:
        training.state = True

    for experience in worker.experiences:
        experience.state = True

    worker_db = Worker(
        identification=worker.identification,
        name=worker.name,
        position_id=worker.position_id,
        department_id=worker.department_id,
        recommended_id=worker.recommended_id,
        wage=worker.wage,
        initial_date=worker.initial_date,
        type=worker.type.value,
        worker_competences=list(map(lambda wc: WorkerCompetence(competence_id=wc.competence_id, state=wc.state), worker.worker_competences)),
        worker_trainings=list(map(lambda wt: WorkerTraining(training_id=wt.training_id, state=wt.state), worker.worker_trainings)),
        experiences=list(map(lambda e: Experience(company=e.company, position=e.position, description=e.description, initial_date=e.initial_date, end_date=e.end_date, wage=e.wage, worker_id=e.worker_id, state=True), worker.experiences)),
        state=True
    )

    db.add(worker_db)
    db.commit()
    db.refresh(worker_db)

    return WorkerSchema(
        id=worker_db.id,
        identification=worker_db.identification,
        name=worker_db.name,
        position_id=worker_db.position_id,
        department_id=worker_db.department_id,
        recommended_id=worker_db.recommended_id,
        wage=worker_db.wage,
        initial_date=worker_db.initial_date,
        type=WorkerType(worker_db.type),
        worker_competences=list(map(lambda wc: WorkerCompetenceSchema(id=wc.id, worker_id=wc.worker_id, competence_id=wc.competence_id, state=wc.state, competence=CompetenceSchema(id=wc.competence.id, name=wc.competence.name, description=wc.competence.description, state=wc.competence.state)), worker.worker_competences)),
        worker_trainings=list(map(lambda wt: WorkerTrainingSchema(id=wt.id, worker_id=wt.worker_id, training_id=wt.training_id, state=wt.state, training=TrainingSchema(
            id=wt.training.id,
            description=wt.training.description,
            level=TrainingLevel(wt.training.level),
            initial_date=wt.training.initial_date,
            end_date=wt.training.end_date,
            institution=wt.training.institution,
            state=wt.training.state,
        )), worker.worker_trainings)),
        experiences=list(map(lambda e: ExperienceSchema(id=e.id, company=e.company, position=e.position, description=e.description, initial_date=e.initial_date, end_date=e.end_date, wage=e.wage, worker_id=e.worker_id, state=e.state), worker_db.experiences)),
        state=worker_db.state,
    )

@router.put("/update")
def update(worker: WorkerSchema, db: Session = Depends(get_db)):
    worker_db: type[Worker] = db.query(Worker).filter(Worker.id == worker.id and Worker.state).first()

    if worker_db is None:
        raise HTTPException(status_code=404, detail=not_found_message_candidate if worker.type == WorkerType.candidate else not_found_message_employee)

    if any(w.state == True for w in worker_db.workers) and worker.state == False:
        raise  HTTPException(status_code=400, detail=recommended_message)

    for competence in worker.worker_competences:
        competence.state = worker.state

    for training in worker.worker_trainings:
        training.state = worker.state

    for experience in worker.experiences:
        experience.state = worker.state

    worker_db.identification = worker.identification
    worker_db.name = worker.name
    worker_db.position_id = worker.position_id
    worker_db.department_id = worker.department_id
    worker_db.recommended_id = worker.recommended_id
    worker_db.wage = worker.wage
    worker_db.initial_date = worker.initial_date
    worker_db.type = worker.type.value
    worker_db.worker_competences = list(
        map(lambda wc: WorkerCompetence(competence_id=wc.competence_id, state=wc.state), worker.worker_competences))
    worker_db.worker_trainings = list(map(lambda wt: WorkerTraining(training_id=wt.training_id, state=wt.state), worker.worker_trainings))
    worker_db.experiences = list(map(lambda e: Experience(company=e.company, position=e.position, description=e.description,
                                                initial_date=e.initial_date, end_date=e.end_date, wage=e.wage,
                                                worker_id=e.worker_id, state=True), worker.experiences))
    worker_db.state = worker.state

    db.commit()
    db.refresh(worker_db)

    return WorkerSchema(
        id=worker_db.id,
        identification=worker_db.identification,
        name=worker_db.name,
        position_id=worker_db.position_id,
        department_id=worker_db.department_id,
        recommended_id=worker_db.recommended_id,
        wage=worker_db.wage,
        initial_date=worker_db.initial_date,
        type=WorkerType(worker_db.type),
        position=PositionSchema(
            id=worker_db.position.id,
            name=worker_db.position.name,
            risk_level=PositionRiskLevel(worker_db.position.risk_level),
            min_wage=worker_db.position.min_wage,
            max_wage=worker_db.position.max_wage,
            state=worker_db.position.state
        ),
        department=DepartmentSchema(id=worker_db.department.id, name=worker_db.department.name,
                                    description=worker_db.department.description, state=worker_db.department.state),
        recommended=None if worker_db.recommended is None else WorkerSchema(
            id=worker_db.recommended.id,
            identification=worker_db.recommended.identification,
            name=worker_db.recommended.name,
            position_id=worker_db.recommended.position_id,
            department_id=worker_db.recommended.department_id,
            recommended_id=worker_db.recommended.recommended_id,
            wage=worker_db.recommended.wage,
            initial_date=worker_db.recommended.initial_date,
            type=WorkerType(worker_db.recommended.type),
            state=worker_db.recommended.state
        ),
        worker_competences=list(map(lambda wc: WorkerCompetenceSchema(id=wc.id, worker_id=wc.worker_id, competence_id=wc.competence_id, state=wc.state, competence=CompetenceSchema(id=wc.competence.id, name=wc.competence.name, description=wc.competence.description, state=wc.competence.state)), worker.worker_competences)),
        worker_trainings=list(map(lambda wt: WorkerTrainingSchema(id=wt.id, worker_id=wt.worker_id, training_id=wt.training_id, state=wt.state, training=TrainingSchema(
            id=wt.training.id,
            description=wt.training.description,
            level=TrainingLevel(wt.training.level),
            initial_date=wt.training.initial_date,
            end_date=wt.training.end_date,
            institution=wt.training.institution,
            state=wt.training.state,
        )), worker.worker_trainings)),
        experiences=list(map(lambda e: ExperienceSchema(id=e.id, company=e.company, position=e.position, description=e.description, initial_date=e.initial_date, end_date=e.end_date, wage=e.wage, worker_id=e.worker_id, state=e.state), worker_db.experiences)),
        state=worker_db.state,
    )