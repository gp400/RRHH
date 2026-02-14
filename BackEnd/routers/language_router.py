from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models.language import Language
from schema.language_schema import LanguageSchema

router = APIRouter()

not_found_message = "Idioma no encontrado."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    languages: list[type[Language]] = db.query(Language).filter(Language.state).all()
    return list(map(lambda language: LanguageSchema(id=language.id, name=language.name, state=language.state), languages))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    language_db: type[Language] = db.query(Language).filter(Language.id == id).first()

    if language_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return LanguageSchema(id=language_db.id, name=language_db.name, state=language_db.state)

@router.post("/create", status_code=201)
def create(language: LanguageSchema, db: Session = Depends(get_db)):
    language_db = Language(name=language.name, state=True)
    db.add(language_db)
    db.commit()
    db.refresh(language_db)
    return LanguageSchema(id=language_db.id, name=language_db.name, state=language_db.state)

@router.put("/update")
def update(language: LanguageSchema, db: Session = Depends(get_db)):
    language_db: type[Language] = db.query(Language).filter(Language.id == language.id and Language.state).first()

    if language_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    language_db.name = language.name
    language_db.state = language.state

    db.commit()
    db.refresh(language_db)

    return LanguageSchema(id=language_db.id, name=language_db.name, state=language_db.state)