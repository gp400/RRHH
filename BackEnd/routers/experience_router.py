from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models.experience import Experience
from schema.experience_schema import ExperienceSchema

router = APIRouter()

not_found_message = "Experiencia no encontrada."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    experiences: list[type[Experience]] = db.query(Experience).filter(Experience.state).all()
    return list(map(lambda experience: ExperienceSchema(
        id=experience.id,
        company=experience.company,
        position=experience.position,
        description=experience.description,
        initial_date=experience.initial_date,
        end_date=experience.end_date,
        wage=experience.wage,
        state=experience.state
    ), experiences))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    experience_db: type[Experience] = db.query(Experience).filter(Experience.id == id).first()

    if experience_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return ExperienceSchema(
        id=experience_db.id,
        company=experience_db.company,
        position=experience_db.position,
        description=experience_db.description,
        initial_date=experience_db.initial_date,
        end_date=experience_db.end_date,
        wage=experience_db.wage,
        state=experience_db.state
    )

@router.post("/create", status_code=201)
def create(experience: ExperienceSchema, db: Session = Depends(get_db)):
    experience_db = Experience(
        id=experience.id,
        company=experience.company,
        position=experience.position,
        description=experience.description,
        initial_date=experience.initial_date,
        end_date=experience.end_date,
        wage=experience.wage,
        state=True
    )
    db.add(experience_db)
    db.commit()
    db.refresh(experience_db)
    return ExperienceSchema(id=experience_db.id, name=experience_db.name, description=experience_db.description, state=experience_db.state)

@router.put("/update")
def update(experience: ExperienceSchema, db: Session = Depends(get_db)):
    experience_db: type[Experience] = db.query(Experience).filter(Experience.id == experience.id and Experience.state).first()

    if experience_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    experience_db.name = experience.name
    experience_db.description = experience.description
    experience_db.state = experience.state

    db.commit()
    db.refresh(experience_db)

    return ExperienceSchema(id=experience_db.id, name=experience_db.name, description=experience_db.description, state=experience_db.state)