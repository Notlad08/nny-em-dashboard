from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

class IncidentCreate(BaseModel):
    timestamp: str
    units: Optional[List[str]] = None
    address: Optional[str] = None
    incident_type: Optional[str] = None
    location: Optional[str] = None
    transcription: Optional[str] = None

class Incident(BaseModel):
    id: str
    timestamp: str
    units: Optional[List[str]] = None
    address: Optional[str] = None
    incident_type: Optional[str] = None
    location: Optional[str] = None
    transcription: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

class IncidentList(BaseModel):
    incidents: List[Incident]
    total: int

@router.post("/", response_model=Incident)
async def create_incident(incident: IncidentCreate):
    """Create a new incident record"""
    incident_id = str(uuid.uuid4())
    return Incident(
        id=incident_id,
        timestamp=incident.timestamp,
        units=incident.units,
        address=incident.address,
        incident_type=incident.incident_type,
        location=incident.location,
        transcription=incident.transcription,
        status="active",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )

@router.get("/", response_model=IncidentList)
async def list_incidents(status: Optional[str] = Query(None), limit: int = Query(100)):
    """List all incidents with optional filtering"""
    # todo: implement database query
    return IncidentList(incidents=[], total=0)

@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    """Get incident by ID"""
    # todo: implement database query
    raise HTTPException(status_code=404, detail="Incident not found")

@router.delete("/{incident_id}")
async def delete_incident(incident_id: str):
    """Delete an incident"""
    # todo: implement database query
    raise HTTPException(status_code=404, detail="Incident not found")

@router.get("/{incident_id}/timeline")
async def get_incident_timeline(incident_id: str, limit: int = Query(100)):
    """Get timeline events for an incident"""
    # todo: implement database query
    return []
