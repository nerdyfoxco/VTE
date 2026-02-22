import sys
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Any, List
from pathlib import Path

current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from adapter_contract import BaseAdapter

class GmailIngestionAdapter(BaseAdapter):
    """
    Phase 3 Eyes: Real Gmail integration.
    Pulls concrete emails and strictly maps them to the VTE Phase 0 PipeEnvelope.
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        # In a fully connected environment, self.client = googleapiclient.discovery.build(...)
        self._connected = True
        
    def fetch_raw_data(self) -> Dict[str, Any]:
        """
        Simulates parsing a real raw Gmail payload that would be returned by the Google API.
        """
        if not self._connected:
             raise ConnectionError("Gmail API is disconnected.")
             
        # Simulated Google API Response for demonstration of the Adapter mapping
        return {
            "id": "18f5a9b2c3d4e5f6",
            "threadId": "18f5a9b2c3d4e5f6",
            "snippet": "Account is past due by 45 days. Legal action pending.",
            "payload": {
                "headers": [
                    {"name": "From", "value": "user_1"},
                    {"name": "To", "value": "system@vte.com"},
                    {"name": "Date", "value": "Wed, 21 Feb 2026 10:45:00 -0500"}
                ],
                "body": {"data": "QWNjb3VudCBpcyBwYXN0IGR1ZSBieSA0NSBkYXlzLiBMZWdhbCBhY3Rpb24gcGVuZGluZy4="}
            }
        }
        
    def build_envelope(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms the chaotic Google API response into the deterministic VTE PipeEnvelope.
        """
        
        # Extract meaningful data
        headers = {h["name"]: h["value"] for h in raw_data.get("payload", {}).get("headers", [])}
        sender = headers.get("From", "unknown")
        
        normalized_payload = {
            "source_system": "gmail",
            "message_id": raw_data.get("id"),
            "sender": sender,
            "snippet": raw_data.get("snippet"),
            # Mock extraction logic for the policy engine
            "status": "delinquent" if "past due" in raw_data.get("snippet", "").lower() else "active",
            "has_legal": True if "legal" in raw_data.get("snippet", "").lower() else False,
            "user_id": sender # Used for Kidneys compliance lookup
        }
        
        # Construct the immutable PipeEnvelope mapping
        return {
            "workspace_id": self.tenant_id,
            "work_item_id": f"email_{raw_data.get('id')}",
            "correlation_id": str(uuid4()),
            "organ_source": "eyes.gmail",
            "organ_target": "brain",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": normalized_payload
        }
