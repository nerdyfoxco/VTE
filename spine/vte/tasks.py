from vte.worker import celery_app
import time
from vte.agents.ingest import IngestionAgent
from vte.agents.auditor import AuditorAgent

# ... (debug tasks)

@celery_app.task(name="agents.ingest.run_once")
def run_ingest_agent():
    """
    Periodic task to run the Ingestion Agent.
    """
    agent = IngestionAgent()
    return agent.run()

@celery_app.task(name="agents.auditor.audit_unit")
def run_auditor_agent(unit_id: str = "101"):
    """
    Task to audit a specific unit.
    """
    agent = AuditorAgent()
    return agent.run(unit_id=unit_id)
def ping():
    """
    Simple task to verify worker connectivity.
    """
    return "pong"

@celery_app.task(name="debug.sleep")
def sleep_task(seconds: int):
    """
    Simulate work.
    """
    time.sleep(seconds)
    return f"Slep for {seconds}s"
