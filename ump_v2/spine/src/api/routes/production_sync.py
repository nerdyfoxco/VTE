import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

# Import the VTE Spine Database and Core Pipe Engine
from db.database import get_db

# Import the newly created Playwright Eyes Adapter
import sys
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(base_dir / "chapters" / "eyes" / "src"))
from appfolio_scraper import AppFolioLiveAdapter

router = APIRouter(prefix="/api/production", tags=["Go-To-Market Integration"])

# In production, these would be retrieved from a secure HashiCorp Vault or AWS Secrets Manager
MOCK_TENANT_ID = "vte_tenant_prod_001"
# The API exposes an async trigger that a CRON job (e.g., AWS EventBridge) hits daily.
async def run_live_scraper_and_ingest(tenant_url_suffix: str, db: AsyncSession):
    try:
        # 1. Spin up the Playwright Scraper
        # (Using dummy credentials for safety in the repository)
        scraper = AppFolioLiveAdapter(
            tenant_id=MOCK_TENANT_ID,
            email="service_account@vte.com",
            password="SECURE_VAULT_PASSWORD",
            base_url="https://demo.appfolio.com"
        )
        
        # 2. Extract DOM nodes into structured Data (Synchronous Playwright execution)
        # Note: In a pure async FastAPI loop, long sync tasks should be sent to a Celery worker.
        # For this integration phase, we execute it directly.
        raw_scraped_data = scraper.fetch_and_map_ledger(tenant_url_suffix)
        
        # 3. Construct the strict Pydantic VTE Envelope
        work_item_id = str(uuid.uuid4())
        envelope_payload = {
            "workspace_id": MOCK_TENANT_ID,
            "work_item_id": work_item_id,
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "playwright_appfolio_scraper",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": raw_scraped_data
        }
        
        # 4. Feed the live payload into the Core VTE Engine
        # The engine will Redact -> Verify Idempotency -> Check Compliance -> Execute Rule Workflow
        from main import internal_process_envelope
        engine_result = await internal_process_envelope(envelope_payload, db)
        
        # 5. Output the result into the VTE Trace Logs
        print(f"[Production Sync] Ledger {tenant_url_suffix} processed. Action: {engine_result['action']}")
        
    except Exception as e:
        print(f"[Production Sync ERROR] Integration failed: {str(e)}")


@router.post("/trigger-appfolio-sync")
async def trigger_live_sync(background_tasks: BackgroundTasks, tenant_url_suffix: str = "ledgers/12345", db: AsyncSession = Depends(get_db)):
    """
    SaaS GTM Endpoint. 
    Accepts a CRON request to sync a specific PM's AppFolio ledger.
    Forks the Playwright Scraper into a Background Task to prevent HTTP timeouts.
    """
    # Push the heavily synchronous Playwright execution to the background
    background_tasks.add_task(run_live_scraper_and_ingest, tenant_url_suffix, db)
    
    return {
        "status": "Accepted", 
        "message": f"Live AppFolio Scraper dispatched for {tenant_url_suffix}. Check the VTE Operator Dashboard Traces for the engine outcome."
    }
