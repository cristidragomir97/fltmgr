from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()

PORTAINER_API = os.getenv("PORTAINER_API", "http://localhost:9000/api")
PORTAINER_TOKEN = os.getenv("PORTAINER_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {PORTAINER_TOKEN}"}

@router.get("/endpoints")
def list_endpoints():
    r = httpx.get(f"{PORTAINER_API}/endpoints", headers=HEADERS)
    return r.json()

@router.get("/containers/{endpoint_id}")
def list_containers(endpoint_id: int):
    r = httpx.get(f"{PORTAINER_API}/endpoints/{endpoint_id}/docker/containers/json", headers=HEADERS)
    return r.json()

@router.post("/containers/{id}/start")
def start_container(id: str):
    r = httpx.post(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/start", headers=HEADERS)
    if r.status_code != 204:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return {"status": "started"}

@router.post("/containers/{id}/stop")
def stop_container(id: str):
    r = httpx.post(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/stop", headers=HEADERS)
    if r.status_code != 204:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return {"status": "stopped"}

@router.get("/containers/{id}/logs")
def container_logs(id: str):
    r = httpx.get(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/logs?stdout=true&stderr=true&tail=100", headers=HEADERS)
    return {"logs": r.text}

@router.get("/containers/{id}/stats")
def container_stats(id: str):
    r = httpx.get(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/stats?stream=false", headers=HEADERS)
    return r.json()
