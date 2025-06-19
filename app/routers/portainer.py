from fastapi import APIRouter
import httpx

from app.portainer_utils import PORTAINER_API, HEADERS

router = APIRouter()

@router.get("/endpoints")
def list_endpoints():
    r = httpx.get(f"{PORTAINER_API}/endpoints", headers=HEADERS)
    return r.json()

@router.get("/endpoints/{endpoint_id}/containers")
def list_containers(endpoint_id: int):
    r = httpx.get(
        f"{PORTAINER_API}/endpoints/{endpoint_id}/docker/containers/json",
        headers=HEADERS,
    )
    return r.json()

