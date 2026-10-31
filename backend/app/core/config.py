from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-20b"
    frontend_origin: str = "http://localhost:3000"
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    youtube_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
