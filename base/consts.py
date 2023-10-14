import os

from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")
BASE_URL = os.getenv("BASE_URL")
STREAM_URL = os.getenv("STREAM_URL")
