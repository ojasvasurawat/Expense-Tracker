import os
from dotenv import load_dotenv
import redis.asyncio as redis

load_dotenv()

REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASS = os.getenv("REDIS_PASS")

client = redis.Redis(
    host="redis-11947.c15.us-east-1-2.ec2.cloud.redislabs.com",
    port=11947,
    username=REDIS_USERNAME,
    password=REDIS_PASS,
    decode_responses=True
)