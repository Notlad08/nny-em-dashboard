from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str

@router.get("/health")
async def health():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="0.1.0")
