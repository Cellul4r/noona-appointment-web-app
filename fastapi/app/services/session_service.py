from datetime import datetime
from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_, or_, select
from app.schemas.session import (
    SessionPrivate,
    SessionUpdate,
)
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.event import Event
from app.models.user import User
from app.db import get_db
from app.models.session_registration import RegistrationStatus, SessionRegistration

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate


class SessionService:
    def __init__(self):
        pass

    # get the session by session_id and check authorized user is the host of the session
    def get_session_by_id(
        self, session_id: int, user_id: int, db: Session
    ) -> SessionModel:
        session = (
            db.execute(
                select(SessionModel)
                .join(Event)
                .where(SessionModel.id == session_id, Event.owner_id == user_id)
            )
            .scalars()
            .first()
        )
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or not authorized",
            )

        return session

    def get_upcoming_sessions_by_event_uuid(
        self,
        event_uuid: uuid.UUID,
        db: Session,
        now: datetime | None = None,
        cursor: str | None = None,
        size: int = 10,
    ) -> tuple[SessionModel, int | None, int | None]:
        if not now:
            now = datetime.utcnow()

        query = (
            select(SessionModel)
            .where(
                SessionModel.end_datetime >= now,
                SessionModel.event.has(Event.share_uuid == event_uuid),
            )
            .order_by(SessionModel.start_datetime.asc(), SessionModel.id.asc())
        )

        cursor_params = CursorParams(cursor=cursor, size=size)

        return paginate(db, query, params=cursor_params)

    def get_past_sessions_by_event_uuid(
        self,
        event_uuid: uuid.UUID,
        db: Session,
        now: datetime | None = None,
        cursor: str | None = None,
        size: int = 10,
    ) -> CursorPage[SessionPrivate]:

        if not now:
            now = datetime.utcnow()

        query = (
            select(SessionModel)
            .where(
                SessionModel.end_datetime < now,
                SessionModel.event.has(Event.share_uuid == event_uuid),
            )
            .order_by(SessionModel.start_datetime.desc(), SessionModel.id.desc())
        )

        cursor_params = CursorParams(cursor=cursor, size=size)

        return paginate(db, query, params=cursor_params)

    # get sessions within a date range and filter by registration status
    def get_all_sessions(
        self,
        user_id: int,
        db: Annotated[Session, Depends(get_db)],
        start_from: datetime | None = None,
        end_to: datetime | None = None,
        scope: str = "all",  # all | joined | hosted
    ) -> list[SessionModel]:

        if scope == "joined":
            stmt = (
                select(SessionModel)
                .join(SessionRegistration)
                .where(SessionRegistration.user_id == user_id)
            )
        elif scope == "hosted":
            stmt = (
                select(SessionModel)
                .join(SessionModel.event)
                .where(Event.owner_id == user_id)
            )
        else:
            stmt = select(SessionModel).where(
                or_(
                    SessionModel.event.has(Event.owner_id == user_id),
                    SessionModel.sessions_registered.any(
                        and_(
                            SessionRegistration.user_id == user_id,
                            SessionRegistration.status == RegistrationStatus.CONFIRMED,
                        )
                    ),
                )
            )

        if start_from:
            stmt = stmt.where(SessionModel.end_datetime >= start_from)
        if end_to:
            stmt = stmt.where(SessionModel.start_datetime <= end_to)

        return db.execute(stmt).scalars().all()

    def get_session_registrations(
        self,
        session_id: int,
        user_id: int,
        db: Session,
        cursor: str | None = None,
        size: int = 20,
    ):
        session = self.get_session_by_id(session_id, user_id, db)

        query = (
            select(
                User.id,
                User.full_name,
                User.email,
                User.profile_image,
                SessionRegistration.status,
            )
            .join(SessionRegistration, SessionRegistration.user_id == User.id)
            .where(SessionRegistration.session_id == session_id)
            .order_by(User.full_name.asc(), User.id.asc())
        )

        cursor_params = CursorParams(cursor, size)
        return paginate(db, query, cursor_params=cursor_params)

    def update_session(
        self, session_id: int, user_id: int, session: SessionUpdate, db: Session
    ) -> SessionModel:
        existing_session = self.get_session_by_id(session_id, user_id, db)
        if not existing_session:
            raise HTTPException(status_code=404, detail="Session not found")

        update_data = session.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(existing_session, k, v)

        db.commit()
        db.refresh(existing_session)
        return existing_session

    def delete_session(self, session_id: int, user_id: int, db: Session):
        existing_session = self.get_session_by_id(session_id, user_id, db)
        if not existing_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )
        db.delete(existing_session)
        db.commit()
