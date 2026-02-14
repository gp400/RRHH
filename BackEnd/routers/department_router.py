from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models.department import Department
from schema.department_schema import DepartmentSchema

router = APIRouter()

not_found_message = "Departamento no encontrado."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    departments: list[type[Department]] = db.query(Department).filter(Department.state).all()
    return list(map(lambda department: DepartmentSchema(id=department.id, name=department.name, description=department.description, state=department.state), departments))

@router.get("/get_by_id/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    department_db: type[Department] = db.query(Department).filter(Department.id == id).first()

    if department_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return DepartmentSchema(id=department_db.id, name=department_db.name, description=department_db.description, state=department_db.state)

@router.post("/create", status_code=201)
def create(department: DepartmentSchema, db: Session = Depends(get_db)):
    department_db = Department(name=department.name, description=department.description, state=True)
    db.add(department_db)
    db.commit()
    db.refresh(department_db)
    return DepartmentSchema(id=department_db.id, name=department_db.name, description=department_db.description, state=department_db.state)

@router.put("/update")
def update(department: DepartmentSchema, db: Session = Depends(get_db)):
    department_db: type[Department] = db.query(Department).filter(Department.id == department.id and Department.state).first()

    if department_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    department_db.name = department.name
    department_db.description = department.description
    department_db.state = department.state

    db.commit()
    db.refresh(department_db)

    return DepartmentSchema(id=department_db.id, name=department_db.name, description=department_db.description, state=department_db.state)