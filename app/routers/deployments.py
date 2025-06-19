from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from app.database_models import Deployment, get_session
from app.firebase_utils import send_push
import os

router = APIRouter()

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
