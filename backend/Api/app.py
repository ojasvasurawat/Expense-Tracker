import uvicorn
from fastapi import FastAPI, Depends
from fastapi.routing import APIRouter
from DB.db import User, Category, Expense
from sqlmodel import SQLModel, Session, create_engine
from Auth.auth import router
from DB.redis_client import client
from Middleware.middleware import auth

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        await client.ping()
        print("Redis connected successfully")
    except Exception as e:
        print("Redis connection failed:", e)

api_router = APIRouter()




@router.get("/middleware-test")
async def get_expenses(user_id: int = Depends(auth)):
    return {"userId": user_id}



app.include_router(router)


if __name__ == "__app__":
    uvicorn.run("app:app", port=8000, log_level="info")