import sys
import unittest
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from approval_guard import ApprovalGuard, ApprovalRecord, ApprovalStatus, ApprovalRequirementError

class TestApprovalGuard(unittest.TestCase):
    
    def test_not_required_passes(self):
        record = ApprovalRecord(is_required=False, status=ApprovalStatus.NOT_REQUIRED)
        try:
            ApprovalGuard.enforce(record)
        except Exception as e:
            self.fail(f"enforce() raised Exception unexpectedly: {e}")

    def test_required_but_pending_fails(self):
        record = ApprovalRecord(is_required=True, status=ApprovalStatus.PENDING)
        with self.assertRaises(ApprovalRequirementError) as context:
            ApprovalGuard.enforce(record)
        self.assertIn("PENDING", str(context.exception))

    def test_required_but_rejected_fails(self):
        record = ApprovalRecord(is_required=True, status=ApprovalStatus.REJECTED)
        with self.assertRaises(ApprovalRequirementError) as context:
            ApprovalGuard.enforce(record)
        self.assertIn("REJECTED", str(context.exception))
        
    def test_approved_without_audit_metadata_fails(self):
        # Even if status is APPROVED, if there's no approver_id, fail the audit constraint
        record = ApprovalRecord(is_required=True, status=ApprovalStatus.APPROVED, approver_id=None)
        with self.assertRaises(ApprovalRequirementError) as context:
            ApprovalGuard.enforce(record)
        self.assertIn("audit trail", str(context.exception))

    def test_approved_with_metadata_passes(self):
        record = ApprovalRecord(
            is_required=True, 
            status=ApprovalStatus.APPROVED, 
            approver_id="admin_123",
            approval_timestamp="2026-02-21T00:00:00Z"
        )
        try:
            ApprovalGuard.enforce(record)
        except Exception as e:
            self.fail(f"enforce() raised Exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()
