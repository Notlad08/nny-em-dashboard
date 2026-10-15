from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

class TimelineEventCreate(BaseModel):
    incident_id: str
    event_type: str
    message: Optional[str] = None
    timestamp: Optional[str] = None  # defaults to now

class TimelineEvent(BaseModel):
    id: str
    incident_id: str
    timestamp: str
    event_type: str
    message: Optional[str] = None
    metadata: dict

class TimelineList(BaseModel):
    events: List[TimelineEvent]
    total: int

@router.post("/", response_model=TimelineEvent)
async def create_timeline_event(event: TimelineEventCreate):
    """Create a new timeline event for an incident"""
    event_id = str(uuid.uuid4())
    timestamp = event.timestamp or datetime.utcnow().isoformat()
    
    return TimelineEvent(
        id=event_id,
        incident_id=event.incident_id,
        timestamp=timestamp,
        event_type=event.event_type,
        message=event.message,
        metadata={},
    )

@router.get("/", response_model=TimelineList)
async def list_timeline_events(
    incident_id: str,
    event_type: Optional[str] = Query(None),
    limit: int = Query(100),
    offset: int = Query(0)
):
    """List timeline events for an incident"""
    # todo: implement database query
    return TimelineList(events=[], total=0)

@router.get("/{incident_id}/timeline", response_model=TimelineList)
async def get_incident_timeline(
    incident_id: str,
    limit: int = Query(100),
    offset: int = Query(0)
):
    """Get timeline events for a specific incident"""
    # todo: implement database query
    return TimelineList(events=[], total=0)

@router.delete("/{incident_id}/timeline/{event_id}")
async def delete_timeline_event(incident_id: str, event_id: str):
    """Delete a timeline event"""
    # todo: implement database query
    raise HTTPException(status_code=404, detail="Timeline event not found")
