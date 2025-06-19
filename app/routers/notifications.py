from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.firebase_utils import send_push

router = APIRouter()

class PushRequest(BaseModel):
    title: str
    body: str
    token: str

@router.post("/send")
def send_notification(req: PushRequest):
    try:
        message_id = send_push(req.title, req.body, req.token)
        return {"message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
