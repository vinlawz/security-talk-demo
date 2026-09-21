import json
import os
from pathlib import Path
from urllib import request, error


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"


def load_env_file(path: Path):
    values = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            return values
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


ENV_VALUES = load_env_file(ENV_PATH)
PAYMENT_API_KEY = os.environ.get("PAYMENT_API_KEY") or ENV_VALUES.get("PAYMENT_API_KEY")


if not PAYMENT_API_KEY:
    raise RuntimeError("PAYMENT_API_KEY is missing. Add it to .env or set it in the environment.")


req = request.Request(
    "http://127.0.0.1:9000/customers",
    headers={"Authorization": f"Bearer {PAYMENT_API_KEY}"},
)

try:
    with request.urlopen(req, timeout=5) as response:
        payload = json.loads(response.read().decode("utf-8"))
        print(json.dumps(payload, indent=2))
except error.HTTPError as exc:
    print(json.dumps({"status": "error", "code": exc.code, "body": exc.read().decode("utf-8")}, indent=2))
