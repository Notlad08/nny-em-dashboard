from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

class UnitCreate(BaseModel):
    unit_id: str
    callsign: Optional[str] = None

class Unit(BaseModel):
    id: str
    unit_id: str
    callsign: Optional[str] = None
    status: str
    last_known_location: Optional[str] = None
    last_transmission: Optional[str] = None
    created_at: str

class UnitList(BaseModel):
    units: List[Unit]
    total: int

@router.post("/", response_model=Unit)
async def create_unit(unit: UnitCreate):
    """Register a new unit"""
    unit_id = str(uuid.uuid4())
    return Unit(
        id=unit_id,
        unit_id=unit.unit_id,
        callsign=unit.callsign,
        status="available",
        created_at=datetime.utcnow().isoformat(),
    )

@router.get("/", response_model=UnitList)
async def list_units(
    status: Optional[str] = Query(None),
    callsign: Optional[str] = Query(None),
    limit: int = Query(100)
):
    """List all units with optional filtering"""
    # todo: implement database query
    return UnitList(units=[], total=0)

@router.get("/{unit_id}")
async def get_unit(unit_id: str):
    """Get unit by ID"""
    # todo: implement database query
    raise HTTPException(status_code=404, detail="Unit not found")

@router.put("/{unit_id}")
async def update_unit(unit_id: str, unit: Unit):
    """Update unit status or location"""
    # todo: implement database query
    raise HTTPException(status_code=404, detail="Unit not found")

@router.delete("/{unit_id}")
async def delete_unit(unit_id: str):
    """Remove a unit from tracking"""
    # todo: implement database query
    raise HTTPException(status_code=404, detail="Unit not found")
