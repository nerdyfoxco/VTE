from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from spine.db.session import get_db
from spine.db.repositories.cases import CasesRepository
from spine.kernel.domain import CanonicalCase, CaseID, TenantID, Money, CaseStatus
from spine.api.routers.auth import get_current_user
from spine.db.models import User

router = APIRouter()

class CreateCaseRequest(BaseModel):
    title: str
    description: str | None = None
    tenant_id: str | None = None # For dev/testing, optional

class UpdateStatusRequest(BaseModel):
    status: CaseStatus

class UpdateStatusRequest(BaseModel):
    status: CaseStatus

class CaseResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: str
    tenant_id: str
    created_at: datetime | None = None




@router.patch("/{case_id}/status", response_model=CaseResponse)
def update_case_status(
    case_id: str,
    req: UpdateStatusRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    P3-14: Update Case Status.
    Enforces P3-12 Valid Transitions.
    """
    repo = CasesRepository(db)
    
    # 1. Check Existence & Tenant
    case = repo.get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    request_tenant = getattr(request.state, "tenant_id", current_user.tenant_id)
    if case.tenant_id != request_tenant:
        raise HTTPException(status_code=404, detail="Case not found")
        
    # 2. Validate Transition (Domain Logic)
    current_status_enum = CaseStatus(case.status)
    # 2. Validate Transition (Domain Logic)
    current_status_enum = CaseStatus(case.status)
    # Use CanonicalCase logic if possible, or direct dictionary logic
    allowed = CanonicalCase.TRANSITIONS.get(current_status_enum, set())
    
    if req.status not in allowed:
         raise HTTPException(
             status_code=422, 
             detail=f"Invalid Transition: {current_status_enum.value} -> {req.status.value}"
         )

    # 3. Update
    updated_case = repo.update_status(case_id, req.status.value)
    return updated_case

@router.get("/", response_model=list[CaseResponse])
def list_cases(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    P3-03: List Cases (Tenant Scoped).
    """
    repo = CasesRepository(db)
    
    # Resolve Tenant Context
    tenant_id = getattr(request.state, "tenant_id", current_user.tenant_id)
    
    return repo.list_by_tenant(tenant_id, skip=skip, limit=limit)

@router.post("/", response_model=CaseResponse)
def create_case(
    req: CreateCaseRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    P2-11: Create Case Endpoint (Wired to Real Persistence).
    Supports Idempotency via 'Idempotency-Key' header.
    """
    repo = CasesRepository(db)
    idempotency_key = request.headers.get("Idempotency-Key")
    
    # Logic: Use user's tenant if not provided
    tenant_id_val = req.tenant_id or current_user.tenant_id
    
    # Logic: Create ID
    case_id_val = str(uuid.uuid4())
    
    # Logic: Domain Entity Construction
    domain_case = CanonicalCase(
        case_id=CaseID(case_id_val),
        tenant_id=TenantID(tenant_id_val),
        balance=Money(0),
        status="OPEN"
    )
    
    # Persistence
    orm_case = repo.create(domain_case, idempotency_key=idempotency_key)
    
    # Post-Processing: Update fields not in domain constructor but in ORM
    # Note: If Idempotent Return, this acts as Upsert (Update fields to latest payload)
    orm_case.title = req.title
    orm_case.description = req.description
    db.commit()
    db.refresh(orm_case)
    
    return orm_case

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    P3-02: Get Case (Tenant Scoped).
    """
    repo = CasesRepository(db)
    case = repo.get_by_id(case_id)
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    # Tenant Isolation Guard (Fail-Closed)
    request_tenant = getattr(request.state, "tenant_id", None)
    
    # If middleware didn't run (unlikely due to pipeline), check user's tenant
    if not request_tenant:
        request_tenant = current_user.tenant_id
        
    if case.tenant_id != request_tenant:
        # 404 to prevent enumeration of IDs existing in other tenants
        raise HTTPException(status_code=404, detail="Case not found")
        
    return case
