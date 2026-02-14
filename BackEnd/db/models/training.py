from sqlalchemy import Column, Integer, String, Boolean, Date

from db.database import Base

class Training(Base):
    __tablename__ = "Training"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    level = Column(Integer)
    initial_date = Column(Date)
    end_date = Column(Date)
    institution = Column(String)
    state = Column(Boolean)