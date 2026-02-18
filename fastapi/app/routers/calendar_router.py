from datetime import datetime
from typing import Annotated
from fastapi import Depends
from fastapi.routing import APIRouter

from app.models.user import User

from app.dependencies.auth import get_current_user
from app.models.session import Session
from app.models.session_registration import RegistrationStatus

from app.db import get_db
from app.services.session_service import SessionService
from app.schemas.session import SessionPublic


router = APIRouter()

session_service = SessionService()


@router.get("")
def get_sessions(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    scope: str = "all",
) -> list[SessionPublic]:
    return session_service.get_all_sessions(
        user_id=current_user.id,
        db=db,
        start_from=start_datetime,
        end_to=end_datetime,
        scope=scope,
    )
