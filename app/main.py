from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import robots, fleet, introspect, portainer, containers
from app.routers import apps, hosts, deployments, auth, notifications
from app.database_models import create_db_and_tables

load_dotenv(".env", override=True)

app = FastAPI()
create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(robots.router, prefix="/api/v1/robots")
app.include_router(fleet.router, prefix="/api/v1/fleet")
app.include_router(portainer.router, prefix="/api/v1/portainer")
app.include_router(containers.router, prefix="/api/v1/containers")
app.include_router(introspect.router, prefix="/api/v1/introspect")
app.include_router(apps.router, prefix="/api/v1/apps")
app.include_router(hosts.router, prefix="/api/v1/hosts")
app.include_router(deployments.router, prefix="/api/v1/deployments")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(notifications.router, prefix="/api/v1/notifications")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
