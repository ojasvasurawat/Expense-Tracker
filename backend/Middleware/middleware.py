import os
import jwt
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


async def auth(Authorization: str = Header(None)):
    if not Authorization:
        return{"message": "token not found"}

    try:
        payload = jwt.decode(
            Authorization,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload["id"]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, details="Error in authorization")