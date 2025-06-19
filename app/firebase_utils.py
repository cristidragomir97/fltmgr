import os
import firebase_admin
from firebase_admin import credentials, messaging

cred_path = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_admin._apps:
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        try:
            firebase_admin.initialize_app()
        except ValueError:
            pass  # Firebase not configured

def send_push(title: str, body: str, token: str) -> str:
    """Send a push notification to the given FCM token."""
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized")
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    return messaging.send(message)
