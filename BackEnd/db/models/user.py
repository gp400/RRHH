from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "User"

