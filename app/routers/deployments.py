from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List, Dict

from app.database_models import Deployment, App, HostEntry, get_session, ContainerInfo
from app.firebase_utils import send_push
import os
import httpx
from app.portainer_utils import PORTAINER_API, HEADERS
from pydantic import BaseModel

router = APIRouter()


class HostConfigUpdate(BaseModel):
    env: dict | None = None
    devices: list[str] | None = None

@router.get("/", response_model=List[Deployment])
def list_deployments():
    with get_session() as session:
        deps = session.exec(select(Deployment)).all()
        return deps

@router.post("/", response_model=Deployment, status_code=201)
def create_deployment(dep: Deployment):
    with get_session() as session:
        existing = session.get(Deployment, dep.id)
        if existing:
            raise HTTPException(status_code=409, detail="Deployment already exists")
        session.add(dep)
        session.commit()
        session.refresh(dep)

        token = os.getenv("FIREBASE_TEST_TOKEN")
        if token:
            try:
                send_push(
                    title="Deployment Created",
                    body=f"Deployment {dep.id} for robot {dep.robot_id}",
                    token=token,
                )
            except Exception as e:
                print(f"FCM error: {e}")
        return dep


@router.post("/{deployment_id}/start")
def start_deployment(deployment_id: str):
    with get_session() as session:
        dep = session.get(Deployment, deployment_id)
        if not dep:
            raise HTTPException(status_code=404, detail="Deployment not found")
        app = session.get(App, dep.app_id)
        if not app:
            raise HTTPException(status_code=404, detail="App not found")
        hosts = session.exec(select(HostEntry).where(HostEntry.robot_id == dep.robot_id)).all()
        for host in hosts:
            compose = app.compose_templates.get(host.type)
            if not compose:
                continue
            resp = httpx.post(
                f"{PORTAINER_API}/stacks",
                params={"endpointId": host.portainer_endpoint_id},
                headers=HEADERS,
                json={"Name": f"{deployment_id}-{host.name}", "StackFileContent": compose},
            )
            if resp.status_code not in (200, 201):
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            host.stack_id = resp.json().get("Id")
        session.commit()
    return {"status": "started"}


@router.put("/{deployment_id}/hosts/{host_id}/config")
def update_host_config(deployment_id: str, host_id: str, cfg: HostConfigUpdate):
    with get_session() as session:
        dep = session.get(Deployment, deployment_id)
        host = session.get(HostEntry, host_id)
        if not dep or not host:
            raise HTTPException(status_code=404, detail="Not found")
        overrides = dep.env_overrides or {}
        host_override = overrides.get(host_id, {})
        if cfg.env:
            host_override["env"] = cfg.env
        if cfg.devices:
            host_override["devices"] = cfg.devices
        overrides[host_id] = host_override
        dep.env_overrides = overrides
        session.add(dep)
        session.commit()

        if host.stack_id:
            resp = httpx.put(
                f"{PORTAINER_API}/stacks/{host.stack_id}",
                params={"endpointId": host.portainer_endpoint_id},
                headers=HEADERS,
                json={"StackFileContent": ""},
            )
            if resp.status_code >= 400:
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return {"status": "updated"}

@router.get("/{dep_id}", response_model=Deployment)
def get_deployment(dep_id: str):
    with get_session() as session:
        dep = session.get(Deployment, dep_id)
        if not dep:
            raise HTTPException(status_code=404, detail="Deployment not found")
        return dep

@router.delete("/{dep_id}", status_code=204)
def delete_deployment(dep_id: str):
    with get_session() as session:
        dep = session.get(Deployment, dep_id)
        if not dep:
            raise HTTPException(status_code=404, detail="Deployment not found")
        session.delete(dep)
    session.commit()
    return


@router.get("/{deployment_id}/containers", response_model=Dict[str, List[ContainerInfo]])
def list_deployment_containers(deployment_id: str):
    """List containers for all hosts belonging to a deployment's robot."""
    with get_session() as session:
        dep = session.get(Deployment, deployment_id)
        if not dep:
            raise HTTPException(status_code=404, detail="Deployment not found")
        hosts = session.exec(select(HostEntry).where(HostEntry.robot_id == dep.robot_id)).all()
    result: Dict[str, List[ContainerInfo]] = {}
    for host in hosts:
        r = httpx.get(
            f"{PORTAINER_API}/endpoints/{host.portainer_endpoint_id}/docker/containers/json",
            headers=HEADERS,
        )
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        result[host.id] = [
            ContainerInfo(
                id=c.get("Id"),
                names=[n.lstrip("/") for n in c.get("Names", [])],
                image=c.get("Image"),
                state=c.get("State"),
                status=c.get("Status"),
            )
            for c in r.json()
        ]
    return result
