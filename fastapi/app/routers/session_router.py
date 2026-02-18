import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.session_service import SessionService
from app.db import get_db
from app.schemas.session import SessionPrivate
from app.dependencies.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

session_service = SessionService()


@router.patch("/{session_id}", response_model=SessionPrivate)
def update_session(
    session_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user=Depends(get_current_user),
):
    return session_service.update_session(session_id, current_user.id, db)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Annotated[Session, Depends(get_db)]):
    session_service.delete_session(session_id, db)


@router.get("/{session_id}/registrations")
def get_session_registrations(
    session_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    cursor: str | None = None,
    size: int = 10,
):
    pass
