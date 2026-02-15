from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from db.database import Base

class Position(Base):
    __tablename__ = "Positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    risk_level = Column(Integer)
    min_wage = Column(Integer)
    max_wage = Column(Integer)
    state = Column(Boolean)

    workers = relationship("Worker", back_populates="position")