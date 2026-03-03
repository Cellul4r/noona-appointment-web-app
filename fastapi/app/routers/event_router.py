import logging
from re import S
from typing import Annotated
from urllib import response
from uuid import UUID
import uuid

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
    Path,
    status,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate

from app.db import get_db

from app.dependencies.auth import get_current_user, get_optional_user
from app.services.event_service import event_service
from app.models.user import User
from app.models.session import Session as SessionModel
from app.schemas.event import (
    EventCreate,
    EventPublic,
    EventSessionPublic,
    EventUpdate,
    EventPrivate,
)
from app.schemas.session import (
    SessionPublic,
    SessionWithOptionalStatus,
)

from app.services.session_service import SessionService
from app.services.notification_service import NotificationService


logger = logging.getLogger(__name__)
router = APIRouter()
session_service = SessionService()
notification_service = NotificationService()


@router.get("/", response_model=CursorPage[EventPrivate])
def list_events(
    scope: str = "all",
    title: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cursor: str | None = Query(default=None),
    size: int = 10,
):
    """
    List events with pagination.
    Use ?page=1&size=20 in the URL to navigate!
    """
    query = event_service.list_events_query(
        scope=scope, title=title, current_user=current_user
    )

    # Paginate executes the query
    return paginate(db, query, params=CursorParams(cursor=cursor, size=size))


@router.get("/{event_uuid}", response_model=EventPublic)
def get_event(
    event_uuid: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_user),
):
    ev = event_service.get_event(event_uuid, db)
    if not ev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    # If it's a draft and and they does not own it. not authorized (forbidden)
    if ev.is_draft and ev.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return ev


@router.get(
    "/{event_uuid}/sessions", response_model=CursorPage[SessionWithOptionalStatus]
)
def get_event_sessions(
    event_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_optional_user)] = None,
    upcoming_only: bool = False,
    scope: str = "all",
    cursor: str | None = None,
    size: int = 10,
):
    # public route will get registration status only if user is logged in
    user_id = current_user.id if current_user else None
    query = session_service.get_all_sessions_by_event(
        event_uuid, user_id=user_id, scope=scope, upcoming_only=upcoming_only
    )

    # before paginate transform the result to include registration_status for each session
    return paginate(
        db,
        query,
        params=CursorParams(cursor=cursor, size=size),
        transformer=lambda items: [
            SessionWithOptionalStatus(
                **session.__dict__,
                registration_status=status,
            )
            for session, status in items
        ],
    )


@router.post(
    "/{event_uuid}/registration-summary", response_model=list[SessionWithOptionalStatus]
)
def send_registration_summary(
    event_uuid: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session_registrations = session_service.get_registration_summary(
        event_uuid, current_user.id, db
    )
    notification_service.enqueue_registration_summary_job(current_user.id, event_uuid)
    return session_registrations


@router.post(
    "/", response_model=EventSessionPublic, status_code=status.HTTP_201_CREATED
)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        ev = event_service.create_event(event_in, db, current_user)
        return ev
    except Exception as e:
        logger.exception("Failed to create event")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event",
        )


@router.patch("/{event_uuid}", response_model=EventSessionPublic)
def update_event(
    event_in: EventUpdate,
    event_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        ev = event_service.update_event_sessions(event_uuid, event_in, db, current_user)
        return ev
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update event",
        )


@router.delete("/{event_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_uuid: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        deleted = event_service.delete_event(event_uuid, db, current_user)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        return None
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete event",
        )
