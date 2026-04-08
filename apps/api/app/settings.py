import os


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_float_env(name: str, default: float) -> float:
    raw = os.getenv(name, str(default))
    return float(raw)
