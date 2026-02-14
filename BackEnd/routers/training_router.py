from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models.training import Training
from enums.training_level import TrainingLevel
from schema.training_schema import TrainingSchema

router = APIRouter()

not_found_message = "Capacitacion no encontrada."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    trainings: list[type[Training]] = db.query(Training).filter(Training.state).all()
    return list(map(lambda training: TrainingSchema(
        id=training.id,
        description=training.description,
        level=TrainingLevel(training.level),
        initial_date=training.initial_date,
        end_date=training.end_date,
        institution=training.institution,
        state=training.state,
    ), trainings))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    training_db: type[Training] = db.query(Training).filter(Training.id == id).first()

    if training_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return TrainingSchema(
        id=training_db.id,
        description=training_db.description,
        level=TrainingLevel(training_db.level),
        initial_date=training_db.initial_date,
        end_date=training_db.end_date,
        institution=training_db.institution,
        state=training_db.state,
    )

@router.post("/create", status_code=201)
def create(training: TrainingSchema, db: Session = Depends(get_db)):
    training_db = Training(
        description=training.description,
        level=training.level.value,
        initial_date=training.initial_date,
        end_date=training.end_date,
        institution=training.institution,
        state=True,
    )
    db.add(training_db)
    db.commit()
    db.refresh(training_db)
    return TrainingSchema(
        id=training_db.id,
        description=training_db.description,
        level=TrainingLevel(training_db.level),
        initial_date=training_db.initial_date,
        end_date=training_db.end_date,
        institution=training_db.institution,
        state=training_db.state,
    )

@router.put("/update")
def update(training: TrainingSchema, db: Session = Depends(get_db)):
    training_db: type[Training] = db.query(Training).filter(Training.id == training.id and Training.state).first()

    if training_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    training_db.description = training.description
    training_db.level = training.level.value
    training_db.initial_date = training.initial_date
    training_db.end_date = training.end_date
    training_db.institution = training.institution
    training_db.state = training.state

    db.commit()
    db.refresh(training_db)

    return TrainingSchema(
        id=training.id,
        description=training.description,
        level=TrainingLevel(training.level),
        initial_date=training.initial_date,
        end_date=training.end_date,
        institution=training.institution,
        state=training.state,
    )