from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, List, Dict
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
import datetime

# ----------- Models -----------

class Host(SQLModel):
    name: str
    type: str
    portainer_endpoint_id: int

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    username: str
    email: str
    password_hash: str
    is_admin: bool = False
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class App(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    description: str
    owner_id: str
    compose_templates: Dict[str, str] = Field(default_factory=dict, sa_column=Column(JSON))
    default_env: Optional[Dict[str, str]] = Field(default=None, sa_column=Column(JSON))

class HostEntry(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    type: str
    robot_id: str
    portainer_endpoint_id: int
    stack_id: Optional[int] = None
    status: Optional[str] = None

class Deployment(SQLModel, table=True):
    id: str = Field(primary_key=True)
    app_id: str
    robot_id: str
    owner_id: str
    notes: Optional[str] = None
    image_tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    env_overrides: Optional[Dict[str, Dict[str, str]]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    status: str

class Robot(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    ros_domain: int
    agent_host: str
    components: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    hosts: List[Host] = Field(default_factory=list, sa_column=Column(JSON))
    watch_topics: List[str] = Field(default_factory=list, sa_column=Column(JSON))

class DeploymentStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    robot_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    success: bool
    log: str

# ----------- DB Engine & Session -----------

DATABASE_URL = "sqlite:///./robocore.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
