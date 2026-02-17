from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from db.database import Base

class Worker(Base):
    __tablename__ = "Worker"

    id = Column(Integer, primary_key=True, index=True)
    identification = Column(String)
    name = Column(String)
    position_id = Column(Integer, ForeignKey("Positions.id", name='fk_worker_position_id'))
    department_id = Column(Integer, ForeignKey("Department.id", name='fk_worker_department_id'))
    recommended_id = Column(Integer, ForeignKey("Worker.id", name='fk_worker_recommended_id'))
    wage = Column(Integer)
    initial_date = Column(Date)
    type = Column(Integer)
    state = Column(Boolean)

    position = relationship("Position", back_populates="workers")
    department = relationship("Department", back_populates="workers")
    recommended = relationship("Worker", remote_side=[id], back_populates="workers")

    worker_competences = relationship("WorkerCompetence", back_populates="worker")
    worker_trainings = relationship("WorkerTraining", back_populates="worker")
    experiences = relationship("Experience", back_populates="worker")
    workers = relationship("Worker", back_populates="recommended")
    users = relationship("User", back_populates="worker")