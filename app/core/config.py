import os
from dotenv import load_dotenv

load_dotenv()

DATABAES_URL = os.getenv("DATABASE_URL")
# secret key