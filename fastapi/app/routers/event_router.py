import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.db import get_db
from app.dependencies.auth import get_current_user
from app.services.event_service import event_service
from app.models.user import User 
from app.schemas.event import (
    EventCreate,
    EventPublic,
    EventSessionPublic,
    EventUpdate,
)

logger = logging.getLogger(__name__)
router = APIRouter()

def map_owner(event):
    if event:
        event.owner = event.host
    return event


@router.get("/", response_model=Page[EventPublic])
def list_events(
    scope: str | None = Query(default=None),
    title: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user), 
):
    """
    List events with pagination. 
    Use ?page=1&size=20 in the URL to navigate!
    """
    query = event_service.list_events_query(
        scope=scope, 
        title=title, 
        current_user=current_user
    )
    
    # Paginate executes the query and applies map_owner to every item
    return paginate(db, query, transformer=lambda items: [map_owner(e) for e in items])


@router.get("/{event_uuid}", response_model=EventSessionPublic)
def get_event(
    event_uuid: UUID = Path(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ev = event_service.get_event(event_uuid, db)
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if ev.is_draft and (not current_user or ev.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return map_owner(ev)


@router.post("/", response_model=EventSessionPublic, status_code=status.HTTP_201_CREATED)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        ev = event_service.create_event(event_in, db, current_user)
        return map_owner(ev)
    except Exception as e:
        logger.exception("Failed to create event")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create event")

@router.put("/{event_uuid}", response_model=EventSessionPublic)
def update_event(
    event_in: EventUpdate,
    event_uuid: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        ev = event_service.update_event(event_uuid, event_in, db, current_user)
        return map_owner(ev)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update event")

@router.delete("/{event_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_uuid: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        deleted = event_service.delete_event(event_uuid, db, current_user)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return None
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete event")