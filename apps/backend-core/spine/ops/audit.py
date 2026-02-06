from sqlalchemy.orm import Session
from spine.db.models import DBAuditLog
from datetime import datetime

class AuditLogger:
    """
    Gap 116: Audit Logging System.
    Writes immutable events to the audit_logs table.
    """
    @staticmethod
    def log(db: Session, actor: str, action: str, target: str, tenant_id: str = "system"):
        """
        Log an event.
        :param db: Database Session
        :param actor: Who performed the action (username or 'system')
        :param action: What happened (e.g., 'LOGIN_SUCCESS', 'USER_INVITED')
        :param target: What was affected (e.g., 'user:admin', 'queue:123')
        """
        try:
            audit_entry = DBAuditLog(
                actor=actor,
                action=action,
                target=target,
                timestamp=datetime.utcnow(),
                tenant_id=tenant_id
            )
            db.add(audit_entry)
            db.commit()
            print(f"[AUDIT] {actor} -> {action} ({target})")
        except Exception as e:
            print(f"[AUDIT FAILURE] Could not write audit log: {e}")
            db.rollback()
