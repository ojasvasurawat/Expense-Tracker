from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declerative_base

Base = declerative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primery_key=True)
    displayName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

