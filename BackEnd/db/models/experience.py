from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Experience(Base):
    __tablename__ = "Experience"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    position = Column(String)
    description = Column(String)
    initial_date = Column(Date)
    end_date = Column(Date)
    wage = Column(Integer)
    worker_id = Column(Integer, ForeignKey("Worker.id", name='fk_experience_worker_id'))
    state = Column(Boolean)

    worker = relationship("Worker", back_populates="experiences")