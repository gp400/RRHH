from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models.competence import Competence
from schema.competence_schema import CompetenceSchema

router = APIRouter()

not_found_message = "Competencia no encontrada."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    competences: list[type[Competence]] = db.query(Competence).filter(Competence.state).all()
    return list(map(lambda competence: CompetenceSchema(id=competence.id, name=competence.name, description=competence.description, state=competence.state), competences))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    competence_db: type[Competence] = db.query(Competence).filter(Competence.id == id).first()

    if competence_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return CompetenceSchema(id=competence_db.id, name=competence_db.name, description=competence_db.description, state=competence_db.state)

@router.post("/create", status_code=201)
def create(competence: CompetenceSchema, db: Session = Depends(get_db)):
    competence_db = Competence(name=competence.name, description=competence.description, state=True)
    db.add(competence_db)
    db.commit()
    db.refresh(competence_db)
    return CompetenceSchema(id=competence_db.id, name=competence_db.name, description=competence_db.description, state=competence_db.state)

@router.put("/update")
def update(competence: CompetenceSchema, db: Session = Depends(get_db)):
    competence_db: type[Competence] = db.query(Competence).filter(Competence.id == competence.id and Competence.state).first()

    if competence_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    competence_db.name = competence.name
    competence_db.description = competence.description
    competence_db.state = competence.state

    db.commit()
    db.refresh(competence_db)

    return CompetenceSchema(id=competence_db.id, name=competence_db.name, description=competence_db.description, state=competence_db.state)