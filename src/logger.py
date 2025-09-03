# src/logger.py
from loguru import logger
from pathlib import Path
import sys

def configure(log_dir: str = "./logs", level: str = "INFO", json_logs: bool = False):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logger.remove()
    if json_logs:
        logger.add(sys.stdout, level=level, serialize=True)
        logger.add(str(Path(log_dir) / "app.log"), rotation="10 MB", retention="7 days", serialize=True, level=level)
    else:
        logger.add(sys.stdout, level=level, format="<green>{time}</green> | <level>{level}</level> | {message}")
        logger.add(str(Path(log_dir) / "app.log"), rotation="10 MB", retention="7 days", level=level)
    return logger
