from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manages application settings loaded from environment variables.
    """
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    gemini_api_key: str # Added for the Gemini API

    class Config:
        env_file = ".env"

# Create a single instance of the settings to be used throughout the app
settings = Settings()

