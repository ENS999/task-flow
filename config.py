from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV", "production")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")
if ENV == "production" and len(SECRET_KEY) < 32:
    raise RuntimeError("Production SECRET_KEY too weak (need 32+ chars)")

ALGORITHM = "HS256"