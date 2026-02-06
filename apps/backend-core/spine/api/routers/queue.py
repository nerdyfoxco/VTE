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
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "priority",
    order: str = "asc",
    status: Optional[str] = "PENDING",
    priority: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    # Security: Allowlist sort fields
    allowed_sorts = ["priority", "sla_deadline", "title", "created_at"]
    if sort_by not in allowed_sorts:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Allowed: {allowed_sorts}")

    query = db.query(DBQueueItem)
    
    # 1. Apply Filtering
    if status is not None:
        if status.upper() != "ALL":
             query = query.filter(DBQueueItem.status == status.upper())
    
    if priority is not None:
        query = query.filter(DBQueueItem.priority == priority)
        
    if search is not None and search.strip():
        query = query.filter(DBQueueItem.title.ilike(f"%{search}%"))
    
    # 2. Apply Sorting
    sort_attr = getattr(DBQueueItem, sort_by)
    if order == "desc":
        query = query.order_by(sort_attr.desc())
    else:
        query = query.order_by(sort_attr.asc())

    # 3. Apply Pagination
    items = query.offset(skip).limit(limit).all()
    return items
