from typing import Dict, Any, List
from vte.core.agent import Agent
from vte.adapters.google.client import GmailClient
from vte.adapters.appfolio.client import AppFolioClient
from vte.api.schema import EvidenceBundleDraft, EvidenceItem
import hashlib
import json
import requests
import os

class IngestionAgent(Agent):
    """
    Polls data sources and ingests them as Immutable Evidence.
    """
    def __init__(self, agent_id: str = "ingest-01"):
        super().__init__(agent_id)
        self.gmail = GmailClient() # Rely on env vars/default paths
        self.appfolio = AppFolioClient()
        self.api_url = os.getenv("API_URL", "http://spine-api:8000/api/v1")
        # Wait, 'spine-worker' runs celery. 'spine-db' runs postgres.
        # The API runs in... wait. docker-compose says:
        # CMD ["uvicorn", "vte.main:app" ...] in Dockerfile.
        # But in docker-compose, we have 'spine-worker'. Where is the API service?
        # Checking docker-compose...
        pass

    def run(self) -> Dict[str, Any]:
        self.logger.info("Starting Ingestion Run...")
        
        # 1. Fetch Google
        email_items = []
        try:
             emails = self.gmail.fetch_emails(max_results=5)
             for e in emails:
                # Hash logic: simplistic for now
                data_str = json.dumps(e, sort_keys=True)
                sha = hashlib.sha256(data_str.encode()).hexdigest()
                item = self.create_evidence("google-gmail", "email_summary", e, sha)
                email_items.append(item)
        except Exception as e:
            self.logger.error(f"Gmail Fetch Failed: {e}", exc_info=True)
            # Do NOT swallow error silently. But do not crash the agent loop entirely?
            # For Phase 18, we want to see errors.
            # Continue to AppFolio fetch attempt?
            
        # 2. Fetch AppFolio (Mock/Stub)
        ledger_items = []
        try:
            # For demo, let's just fetch one unit
            ledger = self.appfolio.fetch_ledger("101")
            
            if ledger:
                 data_str = json.dumps(ledger, sort_keys=True)
                 sha = hashlib.sha256(data_str.encode()).hexdigest()
                 item = self.create_evidence("appfolio", "general_ledger", ledger, sha)
                 ledger_items.append(item)
        except Exception as e:
            self.logger.error(f"AppFolio Fetch Failed: {e}", exc_info=True)
        
        all_items = email_items + ledger_items
        
        if not all_items:
            self.logger.info("No items found.")
            return {"status": "empty", "count": 0}

        # 3. Create Bundle
        bundle = EvidenceBundleDraft(
            normalization_schema="vte-ingest-v1",
            items=all_items
        )
        
        # 4. Post to API
        try:
            return self._post_bundle(bundle)
        except Exception as e:
            self.logger.error(f"Failed to post bundle to API: {e}", exc_info=True)
            raise e

    def _post_bundle(self, bundle: EvidenceBundleDraft) -> Dict[str, Any]:
        """
        Persist bundle to Spine API.
        """
        url = f"{self.api_url}/evidence"
        self.logger.info(f"Posting Bundle to {url}")
        
        # Use bundle.model_dump() for Pydantic V2
        payload = bundle.model_dump(mode='json') 
        
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        
        self.logger.info(f"Bundle Persisted: {resp.json().get('bundle_id')}")
        return {"status": "success", "ingested": len(bundle.items), "response": resp.json()}

