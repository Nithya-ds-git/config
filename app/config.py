import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

def to_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "on"}

def coerce(key, value):
    if key in {"port", "workers"}:
        return int(value)
    if key == "debug":
        return to_bool(value)
    return str(value)

def load_yaml_config(env_name="development"):
    path = BASE_DIR / f"config.{env_name}.yaml"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data

def load_env_config():
    load_dotenv(BASE_DIR / ".env")

    data = {}
    for key, value in os.environ.items():
        if key == "APP_PORT":
            data["port"] = value
        elif key == "APP_WORKERS":
            data["workers"] = value
        elif key == "APP_DEBUG":
            data["debug"] = value
        elif key == "APP_LOG_LEVEL":
            data["log_level"] = value
        elif key == "APP_API_KEY":
            data["api_key"] = value
        elif key == "NUM_WORKERS":
            data["workers"] = value
    return data

def merge_config(cli_overrides=None):
    config = DEFAULTS.copy()

    yaml_cfg = load_yaml_config("development")
    for k, v in yaml_cfg.items():
        config[k] = v

    env_cfg = {}
    env_cfg.update(load_env_config())
    for k, v in env_cfg.items():
        config[k] = v

    if cli_overrides:
        for k, v in cli_overrides.items():
            config[k] = v

    for k in list(config.keys()):
        config[k] = coerce(k, config[k])

    config["api_key"] = "****"
    return config
