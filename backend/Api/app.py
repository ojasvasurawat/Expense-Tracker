import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from DB.db import User, Category, Expense
from sqlmodel import SQLModel, Session, create_engine
from Auth.auth import router
from DB.redis_client import client

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        await client.ping()
        print("Redis connected successfully")
    except Exception as e:
        print("Redis connection failed:", e)

api_router = APIRouter()

app.include_router(router)

# user_1 = User(displayName="xyz", email="xyz@gmail.com", password="xyz", sub=None, income=200000)
# DATABASE_URL = "postgresql://postgres:postgres,123;@localhost:5432/Expense-Tracker"
# engine = create_engine(DATABASE_URL)

# SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     print("Working...")
#     session.add(user_1)
#     session.commit()


# app.post("/signup")(signUp)


if __name__ == "__app__":
    uvicorn.run("app:app", port=8000, log_level="info")