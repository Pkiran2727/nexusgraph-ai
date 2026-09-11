import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip("'\"")

load_env()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PORT = int(os.environ.get("PORT", "8095"))
HOST = os.environ.get("HOST", "0.0.0.0")

if not GEMINI_API_KEY:
    print("[Config Warning] GEMINI_API_KEY is not set in environment or .env file.")
