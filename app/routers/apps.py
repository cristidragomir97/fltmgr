from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from app.database_models import App, get_session

router = APIRouter()

@router.get("/", response_model=List[App])
def list_apps():
    with get_session() as session:
        apps = session.exec(select(App)).all()
        return apps

@router.post("/", response_model=App, status_code=201)
def create_app(app: App):
    with get_session() as session:
        existing = session.get(App, app.id)
        if existing:
            raise HTTPException(status_code=409, detail="App already exists")
        session.add(app)
        session.commit()
        session.refresh(app)
        return app

@router.get("/{app_id}", response_model=App)
def get_app(app_id: str):
    with get_session() as session:
        app_obj = session.get(App, app_id)
        if not app_obj:
            raise HTTPException(status_code=404, detail="App not found")
        return app_obj

@router.put("/{app_id}", response_model=App)
def update_app(app_id: str, updated: App):
    with get_session() as session:
        app_obj = session.get(App, app_id)
        if not app_obj:
            raise HTTPException(status_code=404, detail="App not found")
        updated.id = app_id
        session.merge(updated)
        session.commit()
        return updated

@router.delete("/{app_id}", status_code=204)
def delete_app(app_id: str):
    with get_session() as session:
        app_obj = session.get(App, app_id)
        if not app_obj:
            raise HTTPException(status_code=404, detail="App not found")
        session.delete(app_obj)
        session.commit()
        return
