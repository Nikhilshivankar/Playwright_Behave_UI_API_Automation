import logging
from pathlib import Path
from config.settings import settings

# Define paths relative to the project structure
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "reports"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "run.log"

def get_logger(name: str = "Framework") -> logging.Logger:
    """
    Configures and returns a Logger instance.
    Logs are written to both standard output (console) and a structured run.log file.
    """
    logger = logging.getLogger(name)
    
    # If the logger is already configured, return it to prevent duplicate handler output
    if logger.hasHandlers():
        return logger

    # Set base logging level from configuration settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Formatting structure: Timestamp | Log Level | Message (Filename:Line)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler: capturing debug logs for in-depth execution details
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # Always log verbose debug statements to file
    logger.addHandler(file_handler)

    # Console Handler: capturing real-time logging based on user settings
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    return logger

# Instantiate a default framework logger
logger = get_logger()
