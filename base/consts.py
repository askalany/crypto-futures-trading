import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(key: str) -> str:
    if result := os.getenv(key):
        return result
    raise KeyError(f"Environment variable {key} is not set")


KEY = get_env_var("KEY")
SECRET = get_env_var("SECRET")
BASE_URL = get_env_var("BASE_URL")
STREAM_URL = get_env_var("STREAM_URL")
