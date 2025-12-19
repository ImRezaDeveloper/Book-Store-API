from loguru import logger
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

# console log
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# file log (all)
logger.add(
    LOG_DIR / "app.log",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
)

# file log (errors only)
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="5 MB",
    retention="30 days",
)

def get_logger():
    return logger
