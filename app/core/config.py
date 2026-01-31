from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FYERS_APP_ID: str = ""
    FYERS_CLIENT_ID: str = ""
    FYERS_SECRET_KEY: str = ""
    FYERS_REDIRECT_URI: str = ""
    FYERS_TOTP_KEY: str = ""
    PIN: str = ""
    HTTP_PROXY: str = ""
    HTTPS_PROXY: str = ""
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
