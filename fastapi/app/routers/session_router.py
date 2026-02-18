from datetime import datetime
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.services.session_service import SessionService
from app.db import get_db
from app.schemas.session import (
    SessionPrivate,
    SessionPublic,
    SessionWithEventPublic,
    SessionWithOptionalStatus,
)
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.session_registration import RegistrationStatus
from app.models.session import Session as SessionModel

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

session_service = SessionService()


def transform_session(row):
    mapping = row._mapping

    session = mapping[SessionModel]
    status = mapping["status"]

    return SessionWithEventPublic(
        id=session.id,
        start_datetime=session.start_datetime,
        end_datetime=session.end_datetime,
        event=session.event,
        registration_status=status,
    )


@router.get("", response_model=CursorPage[SessionWithEventPublic])
def get_user_sessions(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    scope: str = "all",
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    cursor: str | None = None,
    size: int = 10,
    registration_status_list: list[RegistrationStatus] = Query(
        default=[RegistrationStatus.CONFIRMED]
    ),
):
    query = session_service.get_all_sessions(
        user_id=current_user.id,
        start_from=start_datetime,
        end_to=end_datetime,
        scope=scope,
        registration_status_list=registration_status_list,
    )

    return paginate(
        db,
        query,
        params=CursorParams(
            cursor=cursor,
            size=size,
        ),
        transformer=lambda rows: [transform_session(row) for row in rows],
    )


@router.get("/{session_id}/registrations")
def get_session_registrations(
    session_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    cursor: str | None = None,
    size: int = 10,
):
    pass


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
