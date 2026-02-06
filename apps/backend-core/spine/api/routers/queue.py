from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from spine.db.engine import get_db
from spine.db.models import DBQueueItem

router = APIRouter()

# Schema derived from contracts/ux/unified_queue_truth_v1.json
class QueueItem(BaseModel):
    id: str
    priority: int
    sla_deadline: datetime
    assigned_to: Optional[str] = None
    title: str # Enriched field for UI
    status: str
    
    class Config:
        from_attributes = True

from spine.api.deps import get_current_active_user
from spine.db.models import DBUser

@router.get("/queue", response_model=List[QueueItem])
def get_queue_items(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    # Real World: Query DB
    items = db.query(DBQueueItem).filter(DBQueueItem.status == "PENDING").all()
    return items
