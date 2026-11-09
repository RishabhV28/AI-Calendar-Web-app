from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str
    LLM_API_KEY: str
    LLM_BASE_URL: str
    LLM_MODEL: str

    class Config:
        env_file =".env"

settings=Settings()