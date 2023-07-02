from dotenv import load_dotenv

import os


load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not all((DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)):
    exit("Specify database properties in .env file")
