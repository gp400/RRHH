from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class WorkerCompetence(Base):
    __tablename__ = "WorkerCompetence"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("Worker.id", name='fk_workercompetence_worker_id'))
    competence_id = Column(Integer, ForeignKey("Competence.id", name='fk_workercompetence_competence_id'))

    worker = relationship("Worker", back_populates="worker_competences")
    competence = relationship("Competence", back_populates="worker_competences")