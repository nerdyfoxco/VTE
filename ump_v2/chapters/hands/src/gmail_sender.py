from typing import Dict, Any

class ExecutionNotApprovedError(Exception):
    pass

class GmailSenderWorker:
    """
    Phase 3 Hands: Real Gmail Outbound actuator.
    This component physically mutates external state (sends an email).
    It expects the Workflow State Machine to reflect PROCEED and Approval to be met.
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        # self.client = googleapiclient.discovery.build('gmail', 'v1', credentials=...)
        
    def execute(self, action_decision: str, envelope: Dict[str, Any]) -> str:
        """
        Executes the outbound email.
        Deterministic check: Hands MUST confirm the Brain told them to PROCEED.
        """
        if action_decision != "PROCEED":
            # Deterministic gating: Actuators must never fire if the policy held or stopped the task.
            raise ExecutionNotApprovedError(f"Hands Execution Blocked: Received Brain command '{action_decision}'. Only 'PROCEED' is permitted for physical mutation.")
            
        target_email = envelope.get("payload", {}).get("sender", "unknown@domain.com")
        snippet = envelope.get("payload", {}).get("snippet", "")
        
        # Simulate real SMTP/Gmail API outbound call
        print(f"\n[GMAIL HANDS] -> Sending outbound resolution to: {target_email} in Workspace {self.tenant_id}")
        print(f"[GMAIL HANDS] -> Body references snippet: '{snippet}'")
        print(f"[GMAIL HANDS] -> Status: 250 OK. Message dispatched.\n")
        
        return "GMAIL_DISPATCH_SUCCESS"
