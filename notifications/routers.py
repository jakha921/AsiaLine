from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from notifications import schemas
from notifications.schemas import NotificationUpdate
from notifications.services import NotificationService

routers = APIRouter()


@routers.get("/notifications", tags=["notifications"])
async def get_notifications(user_id: int,
                            db: Session = Depends(get_db)):
    """
    Get list of notifications\n
    *if offset and limit None return all notifications*\n
    *if offset and limit not None return notifications between offset and limit.*
    """
    try:
        return NotificationService.get_notifications(db, user_id)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get notification list error")


@routers.put("/notifications", response_model=schemas.Notification, tags=["notifications"])
async def update_notification(notification: NotificationUpdate,
                              db: Session = Depends(get_db)):
    """
    Update notification
    """
    try:
        return NotificationService.update_notification(db, notification)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="update notification error")
