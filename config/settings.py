from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """
    Settings class loads configuration options from environment variables or .env file.
    Pydantic automatically validates and type-casts options.
    """
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Application details
    BASE_URL: str = "https://practicetestautomation.com"
    API_BASE_URL: str = "https://petstore.swagger.io/v2"
    ENVIRONMENT: str = "staging"

    # Browser configurations
    BROWSER: str = "chromium"  # options: chromium, firefox, webkit
    HEADLESS: bool = True
    SLOW_MO: int = 0
    DEFAULT_TIMEOUT: int = 30000

    # Logging levels
    LOG_LEVEL: str = "INFO"

    # Test Data Credentials
    TEST_USERNAME: str = "student"
    TEST_PASSWORD: str = "Password123"

# Instantiate settings for global imports
settings = Settings()
