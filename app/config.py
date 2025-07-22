from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    openai_api_key: str
    weather_api_key: str

    class Config:
        env_file = ".env"

# 🔥 Create the instance so it can be imported across the project
settings = Settings()






