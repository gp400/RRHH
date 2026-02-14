from os import name

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models.position import Position
from enums.position_risk_level import PositionRiskLevel
from schema.position_schema import PositionSchema

router = APIRouter()

not_found_message = "Puesto no encontrado."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    positions: list[type[Position]] = db.query(Position).filter(Position.state).all()
    return list(map(lambda position: PositionSchema(
        id=position.id,
        name=position.name,
        risk_level=PositionRiskLevel(position.risk_level),
        min_wage=position.min_wage,
        max_wage=position.max_wage,
        state=position.state
    ), positions))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    position_db: type[Position] = db.query(Position).filter(Position.id == id).first()

    if position_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return PositionSchema(
        id=position_db.id,
        name=position_db.name,
        risk_level=PositionRiskLevel(position_db.risk_level),
        min_wage=position_db.min_wage,
        max_wage=position_db.max_wage,
        state=position_db.state
    )

@router.post("/create", status_code=201)
def create(position: PositionSchema, db: Session = Depends(get_db)):
    position_db = Position(
        name=position.name,
        risk_level=position.risk_level.value,
        min_wage=position.min_wage,
        max_wage=position.max_wage,
        state=True,
    )
    db.add(position_db)
    db.commit()
    db.refresh(position_db)

    return PositionSchema(
        id=position_db.id,
        name=position_db.name,
        risk_level=PositionRiskLevel(position_db.risk_level),
        min_wage=position_db.min_wage,
        max_wage=position_db.max_wage,
        state=position_db.state
    )

@router.put("/update")
def update(position: PositionSchema, db: Session = Depends(get_db)):
    position_db: type[Position] = db.query(Position).filter(Position.id == position.id and Position.state).first()

    if position_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    position_db.name = position.name
    position_db.risk_level = position.risk_level.value
    position_db.min_wage = position.min_wage
    position_db.max_wage = position.max_wage
    position_db.state = position.state

    db.commit()
    db.refresh(position_db)

    return PositionSchema(
        id=position.id,
        name=position.name,
        risk_level=PositionRiskLevel(position.risk_level),
        min_wage=position.min_wage,
        max_wage=position.max_wage,
        state=position.state
    )