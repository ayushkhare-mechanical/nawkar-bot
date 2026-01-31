from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FYERS_APP_ID: str = ""
    FYERS_CLIENT_ID: str = ""
    FYERS_SECRET_KEY: str = ""
    FYERS_REDIRECT_URI: str = ""
    FYERS_TOTP_KEY: str = ""
    PIN: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
