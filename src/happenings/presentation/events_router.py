from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from happenings.domain.user import User

from .dependency_injection import get_current_user

router = APIRouter()


class Location(BaseModel):
    lat: float
    long: float


class EventCreate(BaseModel):
    name: str
    description: str | None = None
    start_datetime: datetime  # eg: "2023-10-01T10:00:00"
    end_datetime: datetime
    location: Location


class EventCreated(EventCreate):
    organizer: str


@router.post("/events", response_model=EventCreated, status_code=201)
async def create_event(
    request: EventCreate,
    current_user: User = Depends(get_current_user),
) -> EventCreate:
    # TODO: Implement event creation logic in an event service
    print(current_user)
    return EventCreated(**request.model_dump(), organizer=current_user.username)
