import os
import httpx
from dotenv import load_dotenv

load_dotenv(".env", override=True)

PORTAINER_PORT = os.getenv("PORTAINER_PORT", "8080")
PORTAINER_API = os.getenv("PORTAINER_API", f"http://localhost:{PORTAINER_PORT}/api")
PORTAINER_TOKEN = os.getenv("PORTAINER_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {PORTAINER_TOKEN}"}


def api_get(path: str, **kwargs) -> httpx.Response:
    url = f"{PORTAINER_API}{path}"
    return httpx.get(url, headers=HEADERS, **kwargs)


def api_post(path: str, **kwargs) -> httpx.Response:
    url = f"{PORTAINER_API}{path}"
    return httpx.post(url, headers=HEADERS, **kwargs)


def api_put(path: str, **kwargs) -> httpx.Response:
    url = f"{PORTAINER_API}{path}"
    return httpx.put(url, headers=HEADERS, **kwargs)

