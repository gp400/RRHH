from sqlalchemy import Column, Integer, String, Boolean

from db.database import Base

class Department(Base):
    __tablename__ = "Department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    state = Column(Boolean)