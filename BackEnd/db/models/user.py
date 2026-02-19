from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    worker_id = Column(Integer, ForeignKey("Worker.id", name='fk_user_worker_id'))
    state = Column(Boolean)

    worker = relationship("Worker", back_populates="users")
