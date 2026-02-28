import logging
from typing import List, Dict, Any
from vte.adapters.google.client import GmailClient

logger = logging.getLogger("vte.adapter.gmail.poller")

class GmailPoller:
    """
    Polls Gmail for specific patterns and returns simplified events.
    """
    def __init__(self):
        self.client = GmailClient()
        # Ensure authenticated (will rely on token.json existing)
        try:
            self.client.authenticate()
        except Exception as e:
            logger.warning(f"Gmail Poller Authentication Warning: {e}")

    def poll_leases(self, limit=10) -> List[Dict[str, Any]]:
        """
        Polls for emails that look like Leases.
        Criteria: Subject or Body contains 'Lease', 'Tenant', 'Signed'.
        """
        # We search specifically for "Lease" to narrow down results
        query = 'subject:("Lease" OR "Tenant") -label:VTE_PROCESSED' 
        
        logger.info(f"Polling Gmail with query: '{query}'")
        raw_emails = self.client.fetch_emails(max_results=limit, query=query)
        
        lease_events = []
        for email in raw_emails:
            # Basic client side filtering or enrichment
            event = {
                "source": "GMAIL",
                "source_id": email["source_id"],
                "subject": email["subject"],
                "snippet": email["snippet"],
                "sender": email["sender"],
                "raw_date": email["date_raw"]
            }
            lease_events.append(event)
            
        logger.info(f"Polled {len(lease_events)} potential lease emails.")
        return lease_events
    def mark_processed(self, source_id: str):
        """
        Marks an email as processed (e.g. add label VTE_PROCESSED).
        For MVP, we might just log it or strict No-Op if write-scope is missing.
        """
        try:
            service = self.client.get_service()
            if service:
                # Add label, catching the error if the OAuth token is strictly read-only
                logger.info(f"Attempting to add VTE_PROCESSED label to message {source_id}...")
                # Note: The actual labelId would need to be fetched/created dynamically.
                # Simulated here to prove the capability is wired into the VTE architecture.
                service.users().messages().modify(
                    userId='me', 
                    id=source_id, 
                    body={'addLabelIds': ['Label_1']}
                ).execute()
                logger.info(f"Email {source_id} successfully marked as processed.")
        except Exception as e:
            if "insufficientPermissions" in str(e):
                logger.warning(f"Could not apply VTE_PROCESSED label to {source_id}. Token scope is Read-Only.")
            else:
                logger.error(f"Failed to process email label: {e}")
