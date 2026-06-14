from pydantic import BaseModel, EmailStr, Field, ConfigDict
import bcrypt
import jwt
from DB.db import User
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
import random
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.routing import APIRouter
from DB.redis_client import client
from fastapi import HTTPException

load_dotenv()
POSTGRES_URI = os.getenv("POSTGRES_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


router = APIRouter()


conf = ConnectionConfig(
    MAIL_USERNAME = str(SMTP_USER),
    MAIL_PASSWORD = str(SMTP_PASS),
    MAIL_FROM = "ojasva.surawat.dev@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TIMEOUT=60
)




engine = create_engine(POSTGRES_URI)
SQLModel.metadata.create_all(engine)

class UserItem(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    displayName: str | None = Field(default=None, min_length=3, max_length=50)
    email: str | None = Field(default=None, unique=True, min_length=3, max_length=320)
    password: str | None = Field(default=None, max_length=20)
    sub: str | None = Field(default=None)
    income: int


@router.post("/signup")
async def signUp(user: UserItem):
    with Session(engine) as session:
        existingUser = session.query(User).filter(User.email == user.email).scalar()
        if existingUser:
            return {"message": "There is already an account with this email"}

        try:
            if user.sub != "":
                sub_bytes = user.sub.encode('utf-8')
                salt = bcrypt.gensalt(rounds=5)
                hashedSubBytes = bcrypt.hashpw(sub_bytes, salt)
                user.sub = hashedSubBytes.decode('utf-8')
                dbUser = User(
                    displayName=user.displayName,
                    email=user.email,
                    password=user.password,
                    sub=user.sub,
                    income=user.income
                )
                session.add(dbUser)
                session.commit()
                return {"message": "user created successfully"}
            else:
                validationCode = random.randint(100000, 999999)
                print(validationCode)
                try:
                    message = MessageSchema(
                        subject = "Expense Tracker email validation code",
                        recipients = [user.email],
                        body = f"Your validation code is:\n\n{validationCode}\n\nEnter this in your application",
                        subtype = MessageType.plain
                    )
                    fm = FastMail(conf)
                    await fm.send_message(message)
                    await client.set(user.email, validationCode, ex=120)
                    return {"message": "we have send you a code on mail"}
                except Exception as e:
                    print(e)
                    return {"message": "error occure during sending mail"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="error occure in signup")



class Code(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(min_length=6, max_length=6)

@router.post("/verifyCode")
async def verifyCode(user: UserItem, code: Code):
    with Session(engine) as session:
        try:
            password_bytes = user.password.encode('utf-8')
            salt = bcrypt.gensalt(rounds=5)
            hashedPasswordBytes = bcrypt.hashpw(password_bytes, salt)

            originalCode = await client.get(user.email)
            if code.code == originalCode:
                user.password = hashedPasswordBytes.decode('utf-8')
                dbUser = User(
                    displayName=user.displayName,
                    email=user.email,
                    password=user.password,
                    sub=user.sub,
                    income=user.income
                )
                session.add(dbUser)
                session.commit()
                return{"message": "user created"}
            return{"message": "wrong code"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="error occure in verifying cod")
        


class SignInItem(BaseModel):
    email: str
    password: str
    sub: str

@router.post("/signin")
async def signIn(user: SignInItem):
    with Session(engine) as session:
        existingUser = session.query(User).filter(User.email == user.email).scalar()
        if not existingUser:
            return{"message": "user not found"}
        if user.sub != "":
            compare = bcrypt.checkpw(user.sub.encode('utf-8'), existingUser.sub.encode('utf-8'))
            if compare:
                token = jwt.encode({"id": existingUser.id}, JWT_SECRET, algorithm="HS256")
                return{
                    "user":{
                        "id": existingUser.id,
                        "displayName": existingUser.displayName,
                        "email": existingUser.email,
                        "income": existingUser.income
                    },
                    "message": "user signed in successfully",
                    "token": token
                }
            else:
                return{"message": "incorrect credential"}
        else:
            compare = bcrypt.checkpw(user.password.encode('utf-8'), existingUser.password.encode('utf-8'))
            if compare:
                token = jwt.encode({"id": existingUser.id}, JWT_SECRET, algorithm="HS256")
                return{
                    "user":{
                        "id": existingUser.id,
                        "displayName": existingUser.displayName,
                        "email": existingUser.email,
                        "income": existingUser.income
                    },
                    "message": "user signed in successfully",
                    "token": token
                }
            else:
                return{"message": "incorrect credential"}