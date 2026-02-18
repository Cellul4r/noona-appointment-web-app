from typing import List
from uuid import UUID
from sqlalchemy import select, or_, exists
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.event import Event
from app.models.session import Session as SessionModel
from app.schemas.event import EventCreate, EventUpdate
from app.models.session_registration import SessionRegistration
from app.models.user import User


class EventService:
    def list_events_query(
        self,
        scope: str | None = None,
        title: str | None = None,
        current_user: User = None,
    ):
        q = select(Event) 

        # If not logged in, return an empty query immediately.
        if current_user is None:
            return q.where(False) 
        else:
            # Has this user registered for any session in this event?
            has_joined = exists().where(
                SessionModel.event_id == Event.id,
                SessionRegistration.session_id == SessionModel.id,
                SessionRegistration.user_id == current_user.id
            )

            # Cover all 3 scenarios
            # - Hosting (owner_id matches)
            # - Joining (has_joined is True)
            # - Hosting & Joining (Both are true)
            q = q.where(
                or_(
                    Event.owner_id == current_user.id,
                    has_joined
                )
            )
        
        # Optional Title Search
        if title:
            q = q.where(Event.title.ilike(f"%{title}%"))

        # Order by title alphabetically for pagination
        q = q.order_by(Event.title.asc())
        
        return q

    def get_event(self, event_uuid: UUID, db: Session) -> Event | None:
        """Return an Event by its share_uuid."""
        return db.execute(select(Event).where(Event.share_uuid == event_uuid)).scalars().first()

    def create_event(self, event_in: EventCreate, db: Session, owner: User) -> Event:
        try:
            ev = Event(
                title=event_in.title,
                location=event_in.location,
                description=event_in.description,
                is_draft=event_in.is_draft,
                owner_id=owner.id,
                max_sessions_per_user=event_in.max_sessions_per_user,
            )

            db.add(ev)
            db.flush()

            for s in event_in.sessions:
                sess = SessionModel(
                    event_id=ev.id, # Keep using internal ID for foreign keys!
                    start_datetime=s.start_datetime,
                    end_datetime=s.end_datetime,
                    seat_capacity=s.seat_capacity,
                )
                db.add(sess)

            db.commit()
            db.refresh(ev)
            return ev
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Database error")
        
    def update_event(self, event_uuid: UUID, event_in: EventUpdate, db: Session, current_user: User) -> Event:
        ev = self.get_event(event_uuid, db)
        if not ev:
            raise KeyError("Event not found")
        if current_user is None or ev.owner_id != current_user.id:
            raise PermissionError("You don't own this event")
        
        UPDATABLE_FIELDS = {"title", "location", "description", "is_draft", "max_sessions_per_user"}
        for field in event_in.model_fields_set:
            if field in UPDATABLE_FIELDS:
                setattr(ev, field, getattr(event_in, field))

        try:
            db.add(ev)
            db.commit()
            db.refresh(ev)
            return ev
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Database error")

    def delete_event(self, event_uuid: UUID, db: Session, current_user: User) -> bool:
        ev = self.get_event(event_uuid, db)
        if not ev:
            return False 
        if current_user is None or ev.owner_id != current_user.id:
            raise PermissionError("You don't own this event")

        try:
            db.delete(ev)
            db.commit()
            return True
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Database error")
    
event_service = EventService()