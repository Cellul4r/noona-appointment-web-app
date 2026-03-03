from datetime import datetime
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.services.session_service import SessionService
from app.db import get_db
from app.schemas.session import (
    SessionPrivate,
    SessionPublic,
    SessionUpdate,
    SessionWithEventPublic,
    SessionWithOptionalStatus,
)
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.session_registration import RegistrationStatus
from app.models.session import Session as SessionModel

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate

from app.schemas.user import UserPublic, UserWithSessionStatus
from app.services.notification_service import NotificationService

import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

session_service = SessionService()
notification_service = NotificationService()


def transform_session(row):
    mapping = row._mapping

    session = mapping[SessionModel]
    status = mapping["status"]

    return SessionWithEventPublic(
        id=session.id,
        uuid=session.uuid,
        start_datetime=session.start_datetime,
        end_datetime=session.end_datetime,
        event=session.event,
        registration_status=status,
        seat_taken=session.seat_taken,
        seat_capacity=session.seat_capacity,
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


@router.get("/{session_uuid}/users", response_model=CursorPage[UserWithSessionStatus])
def get_registered_users(
    session_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    status: RegistrationStatus | None = None,
    cursor: str | None = None,
    size: int = 10,
):
    session = session_service.get_session_by_uuid(session_uuid, db)
    query = session_service.get_registered_user(session.id, status=status)
    return paginate(
        db,
        query,
        params=CursorParams(cursor=cursor, size=size),
        transformer=lambda items: [
            UserWithSessionStatus(**user.__dict__, registration_status=status)
            for user, status in items
        ],
    )


@router.get("/{session_uuid}", response_model=SessionWithEventPublic)
def get_session_by_uuid(
    session_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    row = session_service.get_session_with_user_status(
        session_uuid, current_user.id, db
    )
    return transform_session(row)


@router.post("/{session_uuid}/registration", response_model=SessionWithEventPublic)
def register_session(
    session_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    reminder_minutes_before: list[int] = Query(default=[], max_length=2),
):
    session = session_service.get_session_by_uuid(session_uuid, db)
    # Register the user of this session
    session_service.register_session(session.id, current_user.id, db)
    row = session_service.get_session_with_user_status(
        session_uuid, current_user.id, db
    )

    # Queue notification job for reminder the user
    if len(reminder_minutes_before) > 0:
        notification_service.enqueue_session_reminder_job(
            current_user.id, session.id, session.start_datetime, reminder_minutes_before
        )
    return transform_session(row)


@router.post("/{session_uuid}/confirm", response_model=SessionWithEventPublic)
def confirm_session(
    session_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = session_service.get_session_by_uuid(session_uuid, db)
    session_service.confirm_session(session.id, current_user.id, db)
    row = session_service.get_session_with_user_status(
        session_uuid, current_user.id, db
    )
    return transform_session(row)


@router.delete(
    "/{session_uuid}/registration",
    status_code=status.HTTP_200_OK,
    response_model=SessionWithEventPublic,
)
def unregister_session(
    session_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = session_service.get_session_by_uuid(session_uuid, db)
    recipients = session_service.unregister_session(
        session.id,
        current_user.id,
        db,
    )
    notification_service.enqueue_waitlist_available_jobs(
        session=session,
        recipient_user_ids=recipients,
    )
    row = session_service.get_session_with_user_status(
        session_uuid, current_user.id, db
    )
    return transform_session(row)


@router.delete(
    "/{session_uuid}/registrations/{user_id}", status_code=status.HTTP_200_OK
)
def unregister_user_from_session(
    session_uuid: uuid.UUID,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = session_service.get_session_by_uuid(session_uuid, db)
    recipients = session_service.unregister_user_from_session(
        session.id,
        current_user.id,
        user_id,
        db,
    )
    notification_service.enqueue_waitlist_available_jobs(
        session=session,
        recipient_user_ids=recipients,
    )


@router.patch("/{session_id}", response_model=SessionPrivate)
def update_session(
    session_id: int,
    session: SessionUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return session_service.update_session(session_id, current_user.id, session, db)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session_service.delete_session(session_id, current_user.id, db)
