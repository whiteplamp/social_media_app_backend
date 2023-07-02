from dotenv import load_dotenv

import os

load_dotenv()

JWT_AUTH_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_AUTH_ALGORITHM = "HS256"
