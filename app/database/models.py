from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    messenger_id = Column(Integer, unique=True)

    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    value = Column(String)
    owner_email = Column(String, ForeignKey("users.email"))

    owner = relationship("User", back_populates="notes")
