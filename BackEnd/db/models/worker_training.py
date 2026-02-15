from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db.database import Base

class WorkerTraining(Base):
    __tablename__ = "WorkerTraining"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("Worker.id", name='fk_workertraining_worker_id'))
    training_id = Column(Integer, ForeignKey("Training.id", name='fk_workertraining_training_id'))
    state = Column(Boolean)

    worker = relationship("Worker", back_populates="worker_trainings")
    training = relationship("Training", back_populates="workers")