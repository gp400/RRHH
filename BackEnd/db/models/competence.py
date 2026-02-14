from sqlalchemy import Column, Integer, String, Boolean

from db.database import Base

class Competence(Base):
    __tablename__ = "Competence"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    state = Column(Boolean)