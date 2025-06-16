from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import robots, fleet, introspect, portainer

app = FastAPI()

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
app.include_router(introspect.router, prefix="/api/v1/introspect")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
