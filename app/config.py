from functools import lru_cache
import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL")
    linkedin_access_token: str | None = os.getenv("LINKEDIN_ACCESS_TOKEN")
    naukri_api_key: str | None = os.getenv("NAUKRI_API_KEY")
    naukri_api_secret: str | None = os.getenv("NAUKRI_API_SECRET")

@lru_cache
def get_settings() -> Settings:
    return Settings()

