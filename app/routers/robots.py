from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database_models import Robot, HostEntry, get_session, ContainerInfo
from typing import List, Dict
import httpx
from app.portainer_utils import PORTAINER_API, HEADERS

router = APIRouter()

@router.get("/", response_model=List[Robot])
def list_robots():
    with get_session() as session:
        robots = session.exec(select(Robot)).all()
        return robots

@router.post("/", response_model=Robot, status_code=201)
def create_robot(robot: Robot):
    with get_session() as session:
        existing = session.get(Robot, robot.id)
        if existing:
            raise HTTPException(status_code=409, detail="Robot already exists")
        session.add(robot)
        session.commit()
        session.refresh(robot)
        return robot

@router.get("/{robot_id}", response_model=Robot)
def get_robot(robot_id: str):
    with get_session() as session:
        robot = session.get(Robot, robot_id)
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")
        return robot

@router.put("/{robot_id}", response_model=Robot)
def update_robot(robot_id: str, updated_robot: Robot):
    with get_session() as session:
        robot = session.get(Robot, robot_id)
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")
        updated_robot.id = robot_id  # enforce ID stability
        session.merge(updated_robot)
        session.commit()
        return updated_robot

@router.delete("/{robot_id}", status_code=204)
def delete_robot(robot_id: str):
    with get_session() as session:
        robot = session.get(Robot, robot_id)
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")
        session.delete(robot)
    session.commit()
    return


@router.get("/{robot_id}/containers", response_model=Dict[str, List[ContainerInfo]])
def list_robot_containers(robot_id: str):
    """Return containers across all hosts attached to the given robot."""
    with get_session() as session:
        robot = session.get(Robot, robot_id)
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")
        hosts = session.exec(select(HostEntry).where(HostEntry.robot_id == robot_id)).all()
    results: Dict[str, List[ContainerInfo]] = {}
    for host in hosts:
        r = httpx.get(
            f"{PORTAINER_API}/endpoints/{host.portainer_endpoint_id}/docker/containers/json",
            headers=HEADERS,
        )
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        results[host.id] = [
            ContainerInfo(
                id=c.get("Id"),
                names=[n.lstrip("/") for n in c.get("Names", [])],
                image=c.get("Image"),
                state=c.get("State"),
                status=c.get("Status"),
            )
            for c in r.json()
        ]
    return results
