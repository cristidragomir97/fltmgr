from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from app.database_models import HostEntry, get_session

router = APIRouter()

@router.get("/", response_model=List[HostEntry])
def list_hosts():
    with get_session() as session:
        hosts = session.exec(select(HostEntry)).all()
        return hosts

@router.post("/", response_model=HostEntry, status_code=201)
def create_host(host: HostEntry):
    with get_session() as session:
        existing = session.get(HostEntry, host.id)
        if existing:
            raise HTTPException(status_code=409, detail="Host already exists")
        session.add(host)
        session.commit()
        session.refresh(host)
        return host

@router.get("/{host_id}", response_model=HostEntry)
def get_host(host_id: str):
    with get_session() as session:
        host = session.get(HostEntry, host_id)
        if not host:
            raise HTTPException(status_code=404, detail="Host not found")
        return host

@router.put("/{host_id}", response_model=HostEntry)
def update_host(host_id: str, updated: HostEntry):
    with get_session() as session:
        host = session.get(HostEntry, host_id)
        if not host:
            raise HTTPException(status_code=404, detail="Host not found")
        updated.id = host_id
        session.merge(updated)
        session.commit()
        return updated

@router.delete("/{host_id}", status_code=204)
def delete_host(host_id: str):
    with get_session() as session:
        host = session.get(HostEntry, host_id)
        if not host:
            raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return
