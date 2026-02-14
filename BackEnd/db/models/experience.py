from sqlalchemy import Column, Integer, String, Boolean, Date
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
    state = Column(Boolean)