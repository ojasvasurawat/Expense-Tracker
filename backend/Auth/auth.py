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

class SignUpItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr = Field(min_length=3, max_length=320)
    displayName: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=20)
    sub: str


@router.post("/signup")
async def signUp(item: SignUpItem):
    with Session(engine) as session:
        existingItem = session.query(User).filter(User.email == item.email).scalar()
        if existingItem:
            return {"message": "There is already an account with this email"}

        try:
            password_bytes = item.password.encode('utf-8')
            salt = bcrypt.gensalt(rounds=5)
            hashedPasswordBytes = bcrypt.hashpw(password_bytes, salt)
            if item.sub != "":
                sub_bytes = item.sub.encode('utf-8')
                salt = bcrypt.gensalt(rounds=5)
                hashedSubBytes = bcrypt.hashpw(sub_bytes, salt)
                item.sub = hashedSubBytes.decode('utf-8')
                session.add(item)
                return {"message": "user created successfully"}
            else:
                validationCode = random.randint(100000, 999999)
                try:
                    message = MessageSchema(
                        subject = "Expense Tracker email validation code",
                        recipients = [item.email],
                        body = f"Your validation code is:\n\n{validationCode}\n\nEnter this in your application",
                        subtype = MessageType.plain
                    )
                    fm = FastMail(conf)
                    await fm.send_message(message)
                    await client.set(item.email, validationCode, ex=120)
                    return {"message": "we have send you a code on mail"}
                except Exception as e:
                    print(e)
                    return {"message": "error occure during sending mail"}
        except Exception as e:
            print(e)