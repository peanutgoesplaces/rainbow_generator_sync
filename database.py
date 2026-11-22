from dotenv import load_dotenv
import os
import sys
from pathlib import Path
import psycopg2

#DATABASE_URL=
# LISTENER_URL=
# LISTENER_TOKEN=



if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

env_file = BASE_DIR / ".env"

load_dotenv(env_file, override=True)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)