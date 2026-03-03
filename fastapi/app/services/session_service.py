from datetime import datetime, timedelta
import datetime as dt
from email.policy import HTTP
import logging
from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, background, status
from sqlalchemy import and_, case, func, literal, or_, select
from app.schemas.session import (
    SessionUpdate,
    SessionWithOptionalStatus,
)
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.session import Session as SessionModel
from app.models.event import Event
from app.models.user import User
from app.models.session_registration import RegistrationStatus, SessionRegistration

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

    def get_session_by_uuid(self, session_uuid: str, db: Session) -> SessionModel:
        session = (
            db.execute(select(SessionModel).where(SessionModel.uuid == session_uuid))
            .scalars()
            .first()
        )
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )
        return session

    def get_session_with_user_status(
        self, session_uuid: uuid.UUID, user_id: int, db: Session
    ):
        row = db.execute(
            select(SessionModel)
            .add_columns(SessionRegistration.status.label("status"))
            .outerjoin(
                SessionRegistration,
                and_(
                    SessionRegistration.session_id == SessionModel.id,
                    SessionRegistration.user_id == user_id,
                ),
            )
            .where(SessionModel.uuid == session_uuid)
            .options(selectinload(SessionModel.event).selectinload(Event.host))
        ).first()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        return row

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
        upcoming_only: bool = False,
        scope: str = "all",  # all | joined | hosted
        registration_status_list: list[RegistrationStatus] = [
            RegistrationStatus.CONFIRMED,
            RegistrationStatus.WAITLIST,
            RegistrationStatus.AVAILABLE,
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
        if upcoming_only:
            query = query.where(
                SessionModel.start_datetime >= start_from or datetime.utcnow()
            )
        elif start_from and end_to:
            query = query.where(
                SessionModel.start_datetime < end_to,
                SessionModel.end_datetime >= start_from,
            )
        elif end_to:
            query = query.where(SessionModel.end_datetime < end_to)
        elif start_from:
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
        scope: str = "all",  # all | joined | hosted
        upcoming_only: bool = False,
        now: datetime | None = None,
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

        if now is None:
            now = datetime.utcnow()

        if upcoming_only:
            query = query.where(SessionModel.start_datetime >= now)

        if user_id:
            # if user_id exists, we need to left join with SessionRegistration table
            # to get the registration status of the user for each session
            query = (
                query.where(or_(Event.owner_id == user_id, Event.is_draft == False))
                .outerjoin(
                    SessionRegistration,
                    and_(
                        SessionRegistration.session_id == SessionModel.id,
                        SessionRegistration.user_id == user_id,
                    ),
                )
                .add_columns(SessionRegistration.status.label("registration_status"))
            )

            if scope == "joined":
                query = query.where(SessionRegistration.status.is_not(None))
            elif scope == "hosted":
                query = query.where(Event.owner_id == user_id)

            query = query.order_by(
                SessionModel.start_datetime.asc(),
                SessionModel.id.asc(),
            )
        else:
            # if not just add a plain column with null value of registration status
            query = query.add_columns(literal(None).label("registration_status"))
            query = query.where(
                Event.is_draft == False
            )  # only completed created event can be viewed by public user
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

    def get_registration_summary(
        self, event_uuid: uuid.UUID, user_id: int, db: Session
    ):
        query = self.get_all_sessions_by_event(
            event_uuid, user_id=user_id, scope="joined"
        )
        session_registration = db.execute(query).all()
        return [
            SessionWithOptionalStatus(
                **session.__dict__,
                registration_status=status,
            )
            for session, status in session_registration
        ]

    def update_session(
        self, session_id: int, user_id: int, session: SessionUpdate, db: Session
    ) -> SessionModel:
        # find existing session and check authorized user is the host of the session
        # only host can update/edit the session

        # update session data
        if session.seat_capacity is not None:
            # need to lock the row for update to prevent race condition when multiple user try to update the same session
            existing_session = db.execute(
                select(SessionModel)
                .where(SessionModel.id == session_id, Event.owner_id == user_id)
                .with_for_update()
            ).scalar_one_or_none()

            if not existing_session:
                raise HTTPException(status_code=404, detail="Session not found")

            if session.seat_capacity < existing_session.seat_taken:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="seat_capacity cannot be less than current seat_taken",
                )

        else:
            existing_session = self.get_session_by_id(session_id, user_id, db)

        if not existing_session:
            raise HTTPException(status_code=404, detail="Session not found")

        try:
            update_data = session.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(existing_session, k, v)

            db.commit()
            db.refresh(existing_session)
            return existing_session
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    def delete_session(self, session_id: int, user_id: int, db: Session):
        # only host can delete the session
        existing_session = self.get_session_by_id(session_id, user_id, db)
        if not existing_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )
        # delete the row in the session table
        try:
            db.delete(existing_session)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    def register_session(self, session_id: int, user_id: int, db: Session):

        # register the user to the session, if the session is full, add to waitlist
        # if the user is already registered, return the same registration status without doing anything
        try:
            session = db.execute(
                select(SessionModel)
                .where(SessionModel.id == session_id)
                .with_for_update()  # race condition
            ).scalar_one_or_none()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            existing_registration = db.execute(
                select(SessionRegistration).where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.user_id == user_id,
                )
            ).scalar_one_or_none()
            if existing_registration:
                return existing_registration
            # if seat available confirm the registration
            if (
                session.seat_capacity is None
                or session.seat_taken < session.seat_capacity
            ):
                # count current registration sessions of this event (max_sessions_per_user)
                event = session.event
                current_registrations = db.execute(
                    select(func.count(SessionRegistration.id)).where(
                        SessionRegistration.session.has(
                            SessionModel.event_id == session.event_id
                        ),
                        SessionRegistration.user_id == user_id,
                        SessionRegistration.status == RegistrationStatus.CONFIRMED,
                    )
                ).scalar_one()
                if (
                    event.max_sessions_per_user is not None
                    and current_registrations >= event.max_sessions_per_user
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User has already registered for {event.max_sessions_per_user} sessions.",
                    )
                new_registration = SessionRegistration(
                    session_id=session_id,
                    user_id=user_id,
                    status=RegistrationStatus.CONFIRMED,
                )
                # update the seat taken of this session
                session.seat_taken += 1
                if session.seat_taken == session.seat_capacity:
                    self.set_waitlist_registrations(session_id, user_id, db)
            else:
                # seat capacity full set to WAITLIST
                new_registration = SessionRegistration(
                    session_id=session_id,
                    user_id=user_id,
                    status=RegistrationStatus.WAITLIST,
                )
            db.add(new_registration)
            db.commit()
            db.refresh(new_registration)
            return new_registration
        except IntegrityError:
            db.rollback()
            # Handle duplicate registration
            existing = db.execute(
                select(SessionRegistration).where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.user_id == user_id,
                )
            ).scalar_one()
            return existing
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    def confirm_session(self, session_id: int, user_id: int, db: Session):
        try:
            # get the session data
            session = db.execute(
                select(SessionModel)
                .where(SessionModel.id == session_id)
                .with_for_update()
            ).scalar_one_or_none()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")

            registration = db.execute(
                select(SessionRegistration)
                .where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.user_id == user_id,
                )
                .with_for_update()
            ).scalar_one_or_none()

            if not registration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registration of this session not found.",
                )

            # already confirmed
            if registration.status == RegistrationStatus.CONFIRMED:
                return registration

            # can not transition status from WAITLIST -> CONFIRMED
            if registration.status == RegistrationStatus.WAITLIST:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Status Waitlist can't be confirm to register.",
                )
            # seat is already fulled
            if (
                session.seat_capacity is not None
                and session.seat_taken >= session.seat_capacity
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Session's capacity is full, can not confirm to register this session",
                )
            # set to confirm status
            event = session.event
            current_registrations = db.execute(
                select(func.count(SessionRegistration.id)).where(
                    SessionRegistration.session.has(
                        SessionModel.event_id == session.event_id
                    ),
                    SessionRegistration.user_id == user_id,
                    SessionRegistration.status == RegistrationStatus.CONFIRMED,
                )
            ).scalar_one()
            if (
                event.max_sessions_per_user is not None
                and current_registrations >= event.max_sessions_per_user
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User has already registered for {event.max_sessions_per_user} sessions.",
                )

            registration.status = RegistrationStatus.CONFIRMED
            session.seat_taken += 1
            if (
                session.seat_capacity is not None
                and session.seat_taken == session.seat_capacity
            ):
                self.set_waitlist_registrations(session_id, user_id, db)

            db.commit()
            db.refresh(registration)
            return registration
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    def unregister_session(
        self,
        session_id: int,
        user_id: int,
        db: Session,
    ) -> list[int]:
        notification_recipients: list[int] = []
        try:
            session = db.execute(
                select(SessionModel)
                .where(SessionModel.id == session_id)
                .with_for_update()
            ).scalar_one_or_none()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")

            registration = db.execute(
                select(SessionRegistration).where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.user_id == user_id,
                )
            ).scalar_one_or_none()

            if not registration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registration of this session not found.",
                )

            # reduce the seat taken from the session
            if (
                registration.status == RegistrationStatus.CONFIRMED
                and session.seat_taken > 0
            ):
                session.seat_taken -= 1

            db.delete(registration)

            # if seat is available let the all user that is waitlist -> available
            if (
                session.seat_capacity is not None
                and session.seat_taken < session.seat_capacity
            ):
                notification_recipients = self.set_available_registrations(
                    session_id,
                    user_id,
                    db,
                )

            db.commit()
            return notification_recipients
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    def unregister_user_from_session(
        self,
        session_id: int,
        current_user_id: int,
        user_id: int,
        db: Session,
    ) -> list[int]:
        notification_recipients: list[int] = []
        try:
            session = db.execute(
                select(SessionModel)
                .where(SessionModel.id == session_id)
                .with_for_update()
            ).scalar_one_or_none()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            registration = db.execute(
                select(SessionRegistration).where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.user_id == user_id,
                )
            ).scalar_one_or_none()

            if not registration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registration of this session not found.",
                )

            # Check if the current user is authorized to unregister this user
            if session.event.owner_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to unregister this user.",
                )

            # reduce the seat taken from the session
            if (
                registration.status == RegistrationStatus.CONFIRMED
                and session.seat_taken > 0
            ):
                session.seat_taken -= 1

            db.delete(registration)

            # if seat is available let the all user that is waitlist -> available
            if (
                session.seat_capacity is not None
                and session.seat_taken < session.seat_capacity
            ):
                notification_recipients = self.set_available_registrations(
                    session_id,
                    user_id,
                    db,
                )

            db.commit()
            return notification_recipients
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    def set_available_registrations(
        self,
        session_id: int,
        user_id: int,
        db: Session,
    ) -> list[int]:
        registrations = (
            db.execute(
                select(SessionRegistration)
                .where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.status == RegistrationStatus.WAITLIST,
                    SessionRegistration.user_id != user_id,
                )
                .with_for_update()
            )
            .scalars()
            .all()
        )
        notification_recipients: list[int] = []
        for r in registrations:
            # transaction set to available status
            r.status = RegistrationStatus.AVAILABLE
            if r.user.email_notifications and (
                r.last_available_notified_at is None
                or dt.datetime.now(dt.timezone.utc) - r.last_available_notified_at
                >= timedelta(hours=1)
            ):
                notification_recipients.append(r.user_id)

        logger.info(
            f"Prepared available-seat notifications for users: {notification_recipients}"
        )
        return notification_recipients

    def set_waitlist_registrations(self, session_id: int, user_id: int, db: Session):
        registrations = (
            db.execute(
                select(SessionRegistration)
                .where(
                    SessionRegistration.session_id == session_id,
                    SessionRegistration.status == RegistrationStatus.AVAILABLE,
                    SessionRegistration.user_id != user_id,
                )
                .with_for_update()
            )
            .scalars()
            .all()
        )
        for r in registrations:
            # transaction set to waitlist status
            r.status = RegistrationStatus.WAITLIST
