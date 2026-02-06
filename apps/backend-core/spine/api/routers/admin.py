from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class AdminActionRequest(BaseModel):
    action: str
    target_user_id: str
    reason: str
    # Dual approval requirement for specific actions
    secondary_approver_id: Optional[str] = None

@router.post("/admin/execute")
def execute_admin_action(request: AdminActionRequest):
    """
    T-0750: Identity Admin Surface.
    Enforces constraints from `contracts/iam/identity_admin_surface_v1.json`.
    """
    
    # constraint 1: IMPERSONATE_USER requires Dual Approval
    if request.action == "IMPERSONATE_USER":
        if not request.secondary_approver_id:
            raise HTTPException(
                status_code=403, 
                detail="IMPERSONATE_USER requires Dual Approval (secondary_approver_id missing)."
            )
        # Mock validation of secondary approver
        if request.secondary_approver_id == request.target_user_id:
             raise HTTPException(
                status_code=400, 
                detail="Secondary approver cannot be the target."
            )

    # constraint 2: RESET_MFA triggers security alert
    if request.action == "RESET_MFA":
        # In a real system, this would emit an event to the security bus
        print(f"[SECURITY ALERT] MFA Reset triggered for {request.target_user_id} by Admin.")
    
    # Allowed actions list validation
    allowed_actions = ["PROVISION_TENANT", "REVOKE_TENANT", "RESET_MFA", "IMPERSONATE_USER"]
    if request.action not in allowed_actions:
         raise HTTPException(status_code=400, detail=f"Action {request.action} not permitted.")

    return {
        "status": "success", 
        "action": request.action, 
        "target": request.target_user_id,
        "audit_proof": "mock_proof_hash_123"
    }
