from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NOT_REQUIRED = "NOT_REQUIRED"

class ApprovalRecord(BaseModel):
    is_required: bool
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver_id: Optional[str] = None
    approval_timestamp: Optional[str] = None

class ApprovalRequirementError(Exception):
    """Raised when an execution is attempted without required approvals."""
    pass

class ApprovalGuard:
    """
    Phase 1 Control Plane: Enforces operator approval before executing any Hands logic.
    """
    @classmethod
    def enforce(cls, record: ApprovalRecord) -> None:
        """
        Validates an ApprovalRecord.
        If approval is required, it MUST be APPROVED. 
        PENDING, REJECTED, or invalid states raise an exception.
        """
        if not record.is_required:
            return  # Safe to proceed

        if record.status != ApprovalStatus.APPROVED:
            raise ApprovalRequirementError(
                f"Execution Blocked: Approval is required but current status is {record.status.name}"
            )
            
        if not record.approver_id:
            raise ApprovalRequirementError(
                "Execution Blocked: Status is APPROVED but missing 'approver_id' for audit trail."
            )
