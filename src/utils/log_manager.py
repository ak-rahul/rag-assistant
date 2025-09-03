import logging
from pathlib import Path
from datetime import datetime
import json

class LogManager:
    def __init__(self, log_dir="./logs", json_logs=True):
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = Path(log_dir) / f"log_{timestamp}.log"
        self.json_logs = json_logs
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )

    def info(self, message, **kwargs):
        if self.json_logs:
            log_entry = {"level": "INFO", "message": message, "extra": kwargs, "timestamp": str(datetime.now())}
            logging.info(json.dumps(log_entry))
        else:
            logging.info(message)

    def error(self, message, **kwargs):
        if self.json_logs:
            log_entry = {"level": "ERROR", "message": message, "extra": kwargs, "timestamp": str(datetime.now())}
            logging.error(json.dumps(log_entry))
        else:
            logging.error(message)
