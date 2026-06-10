from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    displayName: str | None = Field(default=None, min_length=3, max_length=50)
    email: str | None = Field(default=None, unique=True, min_length=3, max_length=320)
    password: str | None = Field(default=None, max_length=20)
    sub: str | None = Field(default=None)
    income: int

class Category(Enum):
    FOOD = "food"
    TRAVEL = "trevel"
    STAY = "stay"
    OTHER = "other"

class Expense(SQLModel, table=True):
    __tablename__ = 'expenses'
    id: int | None = Field(default=None, primary_key=True)
    userId: int = Field(foreign_key="users.id", nullable=False)
    category: Category
    amount: int | None = Field(default=None)
    createdAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)

