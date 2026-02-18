from datetime import datetime
from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_, case, literal, or_, select
from app.schemas.session import (
    SessionPrivate,
    SessionUpdate,
)
from sqlalchemy.orm import Session, selectinload, with_loader_criteria
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
        # find the session and check if the user is the host of this session
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
        now: datetime | None = None,
    ) -> tuple[SessionModel, int | None, int | None]:
        # default current time
        if not now:
            now = datetime.utcnow()

        # get sessions that is upcoming or ongoing (end_datetime >= now)
        # we order by start_datetime and then by id
        query = (
            select(SessionModel)
            .where(
                SessionModel.end_datetime >= now,
                SessionModel.event.has(Event.share_uuid == event_uuid),
            )
            .order_by(SessionModel.start_datetime.asc(), SessionModel.id.asc())
        )

        return query

    def get_past_sessions_by_event_uuid(
        self,
        event_uuid: uuid.UUID,
        now: datetime | None = None,
    ):

        # default current time
        if not now:
            now = datetime.utcnow()

        # get sessions that is already ended
        # we order by start_datetime desc and then by id desc
        # recent ended session show first
        query = (
            select(SessionModel)
            .where(
                SessionModel.end_datetime < now,
                SessionModel.event.has(Event.share_uuid == event_uuid),
            )
            .order_by(SessionModel.start_datetime.desc(), SessionModel.id.desc())
        )

        return query

    # get sessions within a date range and filter by registration status
    def get_all_sessions(
        self,
        user_id: int,
        event_uuid: uuid.UUID | None = None,
        start_from: datetime | None = None,
        end_to: datetime | None = None,
        scope: str = "all",  # all | joined | hosted
        registration_status_list: list[RegistrationStatus] = [
            RegistrationStatus.CONFIRMED,
            RegistrationStatus.WAITLIST,
        ],
    ):
        # get all sessions that user is registered for or hosting, and filter by date range if provided
        # all -> both registered and hosted sessions
        # joined -> only sessions user is registered depends on registration_status_list, default both confirm and waitlist
        # hosted -> only sessions user is hosting

        # base query to get sessions table with registration_status of this user
        # and filter only sessions that are associated with specified event
        base_query = (
            select(SessionModel)
            .add_columns(SessionRegistration.status)
            .join(SessionModel.event)
            .outerjoin(
                SessionRegistration,
                and_(
                    SessionRegistration.session_id == SessionModel.id,
                    SessionRegistration.user_id == user_id,
                    SessionRegistration.status.in_(registration_status_list),
                ),
            )
        )

        # filter only a specific event if provided.
        if event_uuid:
            base_query = base_query.where(Event.share_uuid == event_uuid)

        # if scope joined, filter only sessions that user is really registered include waitlist
        # if scope hosted, filter only sessions that user is hosting
        # else return both
        if scope == "joined":
            query = base_query.where(SessionRegistration.status.is_not(None))
        elif scope == "hosted":
            query = base_query.where(Event.owner_id == user_id)
        else:
            query = base_query.where(
                or_(
                    Event.owner_id == user_id,
                    SessionRegistration.status.is_not(None),
                )
            ).distinct()

        query = query.options(selectinload(SessionModel.event).selectinload(Event.host))

        # also filter by date range if provided
        if end_to:
            query = query.where(SessionModel.start_datetime <= end_to)
        if start_from:
            query = query.where(SessionModel.end_datetime >= start_from)

        # natural order by for sessions
        if start_from:
            query = query.order_by(
                SessionModel.start_datetime.asc(), SessionModel.id.asc()
            )
        elif end_to:
            query = query.order_by(
                SessionModel.start_datetime.desc(), SessionModel.id.desc()
            )
        else:
            query = query.order_by(
                SessionModel.start_datetime.asc(), SessionModel.id.asc()
            )

        return query

    def get_all_sessions_by_event(
        self,
        event_uuid: uuid.UUID,
        user_id: int | None = None,
    ):
        # This function return all sessions of an event,
        # if user_id is provided, also get the registration status of the user for each session,
        # and order by registration status
        # if user_id is not provided, return all sessions without registration status (null)

        # Base query to filter only sessions associated by event_uuid
        query = (
            select(SessionModel)
            .join(SessionModel.event)
            .where(Event.share_uuid == event_uuid)
        )

        if user_id:
            # if user_id exists, we need to left join with SessionRegistration table
            # to get the registration status of the user for each session
            query = query.outerjoin(
                SessionRegistration,
                and_(
                    SessionRegistration.session_id == SessionModel.id,
                    SessionRegistration.user_id == user_id,
                ),
            ).add_columns(SessionRegistration.status.label("registration_status"))

            query = query.order_by(
                case(
                    (SessionRegistration.status == RegistrationStatus.CONFIRMED, 0),
                    (SessionRegistration.status == RegistrationStatus.WAITLIST, 1),
                    else_=2,
                ),
                SessionModel.start_datetime.asc(),
                SessionModel.id.asc(),
            )
        else:
            # if not just add a plain column with null value of registration status
            query = query.add_columns(literal(None).label("registration_status"))
            query = query.order_by(
                SessionModel.start_datetime.asc(), SessionModel.id.asc()
            )

        # both will be order by status (if user_id exists), then by start_datetime asc, then by id asc for paginations
        return query

    def get_registered_user(
        self,
        session_id: int,
        status: RegistrationStatus | None = None,
    ):

        query = (
            select(User, SessionRegistration.status)
            .join(User.sessions_registered)
            .where(SessionRegistration.session_id == session_id)
            .order_by(User.full_name.asc(), User.id.asc())
        )

        if status is not None:
            query = query.where(SessionRegistration.status == status)
        query = query.options(selectinload(User.sessions_registered))
        query = query
        return query

    def update_session(
        self, session_id: int, user_id: int, session: SessionUpdate, db: Session
    ) -> SessionModel:
        # find existing session and check authorized user is the host of the session
        # only host can update/edit the session
        existing_session = self.get_session_by_id(session_id, user_id, db)
        if not existing_session:
            raise HTTPException(status_code=404, detail="Session not found")

        # update session data
        update_data = session.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(existing_session, k, v)

        db.commit()
        db.refresh(existing_session)
        return existing_session

    def delete_session(self, session_id: int, user_id: int, db: Session):
        # only host can delete the session
        existing_session = self.get_session_by_id(session_id, user_id, db)
        if not existing_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )
        # delete the row in the session table
        db.delete(existing_session)
        db.commit()
