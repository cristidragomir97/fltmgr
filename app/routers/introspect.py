from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict
from starlette.websockets import WebSocketState

router = APIRouter()

# Active agent connections
active_agents: Dict[str, WebSocket] = {}

@router.websocket("/ws/robots/{robot_id}")
async def robot_ws(websocket: WebSocket, robot_id: str):
    await websocket.accept()
    active_agents[robot_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            # Handle 'handshake', 'heartbeat', 'ros_data', etc.
            print(f"[agent:{robot_id}] {data}")
    except WebSocketDisconnect:
        print(f"[agent:{robot_id}] disconnected")
        del active_agents[robot_id]

@router.get("/{robot_id}/nodes")
async def get_nodes(robot_id: str):
    agent = active_agents.get(robot_id)
    if not agent or agent.client_state != WebSocketState.CONNECTED:
        raise HTTPException(status_code=503, detail="Agent not connected")
    await agent.send_json({"cmd": "get_nodes"})
    result = await agent.receive_json()
    return result

@router.get("/{robot_id}/topics")
async def get_topics(robot_id: str):
    agent = active_agents.get(robot_id)
    if not agent or agent.client_state != WebSocketState.CONNECTED:
        raise HTTPException(status_code=503, detail="Agent not connected")
    await agent.send_json({"cmd": "get_topics"})
    result = await agent.receive_json()
    return result
