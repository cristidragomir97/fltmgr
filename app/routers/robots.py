from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database_models import Robot, get_session
from typing import List

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
