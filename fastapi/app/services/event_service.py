from uuid import UUID
from fastapi import HTTPException
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
        scope: str = "all",
        title: str | None = None,
        current_user: User = None,
    ):
        q = select(Event)

        # If not logged in, return an empty query immediately.
        if current_user is None:
            q = q.where(False)
        else:
            # Has this user registered for any session in this event?
            has_joined = exists().where(
                SessionModel.event_id == Event.id,
                SessionRegistration.session_id == SessionModel.id,
                SessionRegistration.user_id == current_user.id,
            )

            # Cover all 3 scenarios
            # - Hosting (owner_id matches)
            # - Joining (has_joined is True)
            # - Hosting & Joining (Both are true)
            if scope == "hosted":
                # Only show events I own
                q = q.where(Event.owner_id == current_user.id)

            elif scope == "joined":
                # Only show events I have registered for
                q = q.where(has_joined)

            else:
                # "all" (Default) - Show both
                q = q.where(or_(Event.owner_id == current_user.id, has_joined))

        # Optional Title Search
        if title:
            q = q.where(Event.title.ilike(f"%{title}%"))

        # Order by title alphabetically for pagination
        q = q.order_by(Event.title.asc(), Event.id.asc())

        return q

    def get_event(self, event_uuid: UUID, db: Session) -> Event | None:
        """Return an Event"""
        return db.execute(
            select(Event).where(Event.share_uuid == event_uuid)
        ).scalar_one_or_none()

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
                    event_id=ev.id,  # Keep using internal ID for foreign keys!
                    start_datetime=s.start_datetime,
                    end_datetime=s.end_datetime,
                    location=s.location,
                    seat_capacity=s.seat_capacity or None,
                )
                db.add(sess)

            db.commit()
            db.refresh(ev)
            return ev
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Database error")

    def update_event(
        self,
        event_uuid: UUID,
        event_in: EventUpdate,
        db: Session,
        current_user: User,
        auto_commit: bool = True,
    ) -> Event:
        ev = self.get_event(event_uuid, db)
        if not ev:
            raise KeyError("Event not found")
        if current_user is None or ev.owner_id != current_user.id:
            raise PermissionError("You don't own this event")

        UPDATABLE_FIELDS = {
            "title",
            "location",
            "description",
            "is_draft",
            "max_sessions_per_user",
        }
        for field in event_in.model_fields_set:
            if field in UPDATABLE_FIELDS:
                setattr(ev, field, getattr(event_in, field))

        try:
            db.add(ev)
            if auto_commit:
                db.commit()
                db.refresh(ev)
            return ev
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Database error")

    def update_event_sessions(
        self,
        event_uuid: UUID,
        event_in: EventUpdate,
        db: Session,
        current_user: User,
    ):
        # Update event details and sessions in one transaction
        try:
            ev = self.update_event(
                event_uuid, event_in, db, current_user, auto_commit=False
            )
            # Find default sessions
            existing_sessions = (
                db.execute(
                    select(SessionModel)
                    .where(SessionModel.event_id == ev.id)
                    .with_for_update()
                )
                .scalars()
                .all()
            )
            # Determine which sessions to update, delete, or add
            # if new sessions has an id, if match with existing session -> update
            # else -> add new session
            # if existing session id not in new sessions -> delete
            if event_in.sessions is None:
                # update only event details
                db.commit()
                db.refresh(ev)
                return ev

            for s in event_in.sessions:
                if s.action == "create":
                    new_sess = SessionModel(
                        event_id=ev.id,
                        start_datetime=s.data.start_datetime,
                        end_datetime=s.data.end_datetime,
                        location=s.data.location,
                        seat_capacity=s.data.seat_capacity or None,
                    )
                    db.add(new_sess)
                elif s.action == "update":
                    existing_sess = next(
                        (
                            sess
                            for sess in existing_sessions
                            if sess.uuid == s.session_uuid
                        ),
                        None,
                    )
                    if not existing_sess:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Session {s.session_uuid} not found",
                        )

                    if (
                        existing_sess.seat_taken > 0
                        and s.data.seat_capacity is not None
                        and s.data.seat_capacity < existing_sess.seat_taken
                    ):
                        raise HTTPException(
                            status_code=400,
                            detail=f"Cannot reduce seat capacity below current seat taken count {existing_sess.seat_taken}",
                        )

                    update_data = s.data.model_dump(exclude_unset=True)
                    for field, value in update_data.items():
                        setattr(existing_sess, field, value)

                    db.add(existing_sess)
                elif s.action == "delete":
                    existing_sess = next(
                        (
                            sess
                            for sess in existing_sessions
                            if sess.uuid == s.session_uuid
                        ),
                        None,
                    )
                    if not existing_sess:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Session {s.session_uuid} not found",
                        )
                    db.delete(existing_sess)
            db.commit()
            db.refresh(ev)
            return ev

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error")

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
