from email.policy import HTTP
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
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate

from app.db import get_db

from app.dependencies.auth import get_current_user, get_optional_user
from app.services.event_service import event_service
from app.models.user import User
from app.models.session import Session as SessionModel
from app.models.session_registration import SessionRegistration
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
        old_ev = event_service.get_event(event_uuid, db)
        if not old_ev:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )

        target_user_ids = (
            db.execute(
                select(SessionRegistration.user_id)
                .join(
                    SessionModel,
                    SessionModel.id == SessionRegistration.session_id,
                )
                .where(SessionModel.event_id == old_ev.id)
                .distinct()
            )
            .scalars()
            .all()
        )
        event_change: dict = {}
        if event_in:
            if event_in.title and event_in.title != old_ev.title:
                event_change["title"] = {
                    "old": old_ev.title,
                    "new": event_in.title,
                }
            if event_in.description and event_in.description != old_ev.description:
                event_change["description"] = {
                    "old": old_ev.description,
                    "new": event_in.description,
                }
            if event_in.location and event_in.location != old_ev.location:
                event_change["location"] = {
                    "old": old_ev.location,
                    "new": event_in.location,
                }
            if (
                event_in.max_sessions_per_user
                and event_in.max_sessions_per_user != old_ev.max_sessions_per_user
            ):
                event_change["max_sessions_per_user"] = {
                    "old": old_ev.max_sessions_per_user,
                    "new": event_in.max_sessions_per_user,
                }

        session_changes: list[dict] = []
        if event_in.sessions:
            for operation in event_in.sessions:
                item: dict = {"action": operation.action}
                if (
                    hasattr(operation, "session_uuid")
                    and operation.session_uuid is not None
                ):
                    item["session_uuid"] = str(operation.session_uuid)
                if hasattr(operation, "data") and operation.data is not None:
                    data = operation.data
                    item["start_datetime"] = (
                        data.start_datetime.isoformat()
                        if getattr(data, "start_datetime", None)
                        else None
                    )
                    item["end_datetime"] = (
                        data.end_datetime.isoformat()
                        if getattr(data, "end_datetime", None)
                        else None
                    )
                    item["location"] = getattr(data, "location", None)
                session_changes.append(item)

        ev = event_service.update_event_sessions(event_uuid, event_in, db, current_user)
        notification_service.enqueue_event_updated_jobs(
            event_id=ev.id,
            event_uuid=str(ev.share_uuid),
            event_change=event_change,
            session_changes=session_changes,
            target_user_ids=target_user_ids,
        )
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
        logger.exception("Failed to update event", exc_info=e)
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
