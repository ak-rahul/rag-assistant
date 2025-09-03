
from loguru import logger
from pathlib import Path
import sys

def configure(level: str = "INFO", json: bool = False, log_dir: str = "./logs"):
    p = Path(log_dir)
    p.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level=level, serialize=json, backtrace=True, diagnose=False, enqueue=True)
    logger.add(p / "app.log", level=level, serialize=json, rotation="10 MB", retention="14 days")
    return logger
