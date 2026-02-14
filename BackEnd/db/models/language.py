from sqlalchemy import Column, Integer, String, Boolean

from db.database import Base

class Language(Base):
    __tablename__ = "Language"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    state = Column(Boolean)