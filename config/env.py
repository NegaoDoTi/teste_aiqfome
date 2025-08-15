from dotenv import load_dotenv
from os import getenv

load_dotenv()

PORT = int(getenv("PORT"))
DEBUG = bool(eval(getenv("DEBUG")))
SECRECT_KEY = getenv("SECRECT_KEY")
ALGORITHM = getenv("ALGORITHM")
DATABASE_URL = getenv("DATABASE_URL")