from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status

from app.config import settings
from app.services.notification_service import NotificationService
from app.dependencies.auth import csrf_protect


router = APIRouter()
notification_service = NotificationService()


@router.get("/dispatch")
async def dispatch_notifications(
    request: Request,
    size: int = Query(default=50, ge=1, le=200),
):
    auth_header = request.headers.get("authorization")
    if auth_header != f"Bearer {settings.cron_secret}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid or missing cron secret",
        )

    result = await notification_service.dispatch_pending_jobs(batch_size=size)
    return result
