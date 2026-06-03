from fastapi import FastAPI
from DB.db import User, Category, Expense
from sqlmodel import SQLModel, Session, create_engine

app = FastAPI()

user_1 = User(displayName="xyz", email="xyz@gmail.com", password="xyz", sub=None, income=200000)
DATABASE_URL = "postgresql://postgres:postgres,123;@localhost:5432/Expense-Tracker"
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    print("Working...")
    session.add(user_1)
    session.commit()