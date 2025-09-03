import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def get(self, key_path, default=None):
        keys = key_path.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value == default:
                break
        return value
