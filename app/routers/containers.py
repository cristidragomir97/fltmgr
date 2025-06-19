from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

from app.portainer_utils import PORTAINER_API, HEADERS

router = APIRouter()

class ExecRequest(BaseModel):
    cmd: list[str]

@router.post("/{id}/start")
def start_container(id: str):
    r = httpx.post(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/start", headers=HEADERS)
    if r.status_code != 204:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return {"status": "started"}

@router.post("/{id}/stop")
def stop_container(id: str):
    r = httpx.post(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/stop", headers=HEADERS)
    if r.status_code != 204:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return {"status": "stopped"}

@router.get("/{id}/logs")
def container_logs(id: str, tail: int = 100):
    r = httpx.get(
        f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/logs",
        params={"stdout": "true", "stderr": "true", "tail": tail},
        headers=HEADERS,
    )
    return {"logs": r.text}

@router.get("/{id}/stats")
def container_stats(id: str):
    r = httpx.get(f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/stats", params={"stream": "false"}, headers=HEADERS)
    return r.json()

@router.post("/{id}/exec")
def exec_container(id: str, req: ExecRequest):
    create = httpx.post(
        f"{PORTAINER_API}/endpoints/1/docker/containers/{id}/exec",
        headers=HEADERS,
        json={"AttachStdout": True, "AttachStderr": True, "Tty": False, "Cmd": req.cmd},
    )
    if create.status_code != 201:
        raise HTTPException(status_code=create.status_code, detail=create.text)
    exec_id = create.json().get("Id")
    start = httpx.post(
        f"{PORTAINER_API}/endpoints/1/docker/exec/{exec_id}/start",
        headers=HEADERS,
        json={"Detach": False, "Tty": False},
    )
    if start.status_code != 200:
        raise HTTPException(status_code=start.status_code, detail=start.text)
    return {"output": start.text}
