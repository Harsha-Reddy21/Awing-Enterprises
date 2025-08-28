from functools import lru_cache
import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL")

@lru_cache
def get_settings() -> Settings:
    return Settings()

