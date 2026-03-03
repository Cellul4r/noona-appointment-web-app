from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Query, status

from app.config import settings
from app.services.notification_service import NotificationService


router = APIRouter()
notification_service = NotificationService()


@router.post("/dispatch")
async def dispatch_notifications(
    size: int = Query(default=50, ge=1, le=200),
    x_cron_secret: Annotated[str | None, Header()] = None,
):
    if settings.cron_secret and x_cron_secret != settings.cron_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid cron secret",
        )

    result = await notification_service.dispatch_pending_jobs(batch_size=size)
    return result
