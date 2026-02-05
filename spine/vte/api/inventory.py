from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from vte.db import get_db
from vte.orm import Property, Unit
from typing import List, Optional
from pydantic import BaseModel, UUID4

router = APIRouter()

# --- Schemas (Response Only) ---
class UnitRead(BaseModel):
    unit_id: UUID4
    name: str
    status: str
    external_ref_id: Optional[str]
    tenant_info: Optional[dict]
    
    class Config:
        from_attributes = True

class PropertyRead(BaseModel):
    property_id: UUID4
    name: str
    address: Optional[str]
    units: List[UnitRead] = []

    class Config:
        from_attributes = True

# --- Endpoints ---
@router.get("/properties", response_model=List[PropertyRead])
def get_properties(db: Session = Depends(get_db)):
    """
    Get all properties.
    """
    return db.query(Property).all()

@router.get("/properties/{property_id}", response_model=PropertyRead)
def get_property(property_id: str, db: Session = Depends(get_db)):
    """
    Get specific property + units.
    """
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@router.get("/units", response_model=List[UnitRead])
def get_units(property_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get units, optionally filtered by property.
    """
    query = db.query(Unit)
    if property_id:
        query = query.filter(Unit.property_id == property_id)
    return query.all()

@router.get("/units/{unit_id}", response_model=UnitRead)
def get_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.unit_id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit

# --- Automation Triggers ---
@router.post("/ingest/run")
def trigger_ingestion(db: Session = Depends(get_db)):
    """
    Triggers the Ingestion Agent to poll email and update inventory.
    (Ideally this runs via Celery Beat, but exposed here for Demo/Testing)
    """
    from vte.agents.ingestion import IngestionAgent
    
    agent = IngestionAgent(db)
    # Run synchronously for the trigger response
    agent.run_cycle()
    
    return {"status": "success", "message": "Ingestion Cycle Completed"}
