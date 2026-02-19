from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models.user import User
from enums.worker_type import WorkerType
from helpers.hash_helper import is_hash_matching
from schema.user_schema import UserSchema

router = APIRouter()

SECRET_KEY = "secret_key"      # change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

not_found_message = "Usuario no encontrado."
credentials_invalid = "Credenciales invalidas."
not_permission = "El Usuario no tiene permiso."

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db)):
    user_db: type[User] = db.query(User).filter(User.email == user.email).first()

    if user_db is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    if WorkerType(user_db.worker.type) != WorkerType.employee:
        raise HTTPException(status_code=400, detail=not_permission)

    password_hash = is_hash_matching(user.password, user_db.password)

    if not password_hash:
        raise HTTPException(status_code=400, detail=credentials_invalid)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {
        "id": user_db.id,
        "worker_type": user_db.worker.type,
        "exp": expire
    }

    # 3) Encode a JWT
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return token